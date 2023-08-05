
"""Bloom Filter: Probabilistic set membership testing for large sets."""

# Shamelessly borrowed (under MIT license) from http://code.activestate.com/recipes/577686-bloom-filter/
# About Bloom Filters: http://en.wikipedia.org/wiki/Bloom_filter

# Tweaked by Daniel Richard Stromberg, mostly to:
# 1) Give it a little nicer __init__ parameters.
# 2) Improve the hash functions to get a much lower rate of false positives.
# 3) Give it a selection of backends.
# 4) Make it pass pylint.

import os
import math
import array
import random

try:
    import mmap as mmap_mod
except ImportError:
    # Jython lacks mmap()
    HAVE_MMAP = False
else:
    HAVE_MMAP = True

# In the literature:
# k is the number of probes - we call this num_probes_k
# m is the number of bits in the filter - we call this num_bits_m
# n is the ideal number of elements to eventually be stored in the filter - we call this ideal_num_elements_n
# p is the desired error rate when full - we call this error_rate_p


null_byte = bytes([0])


if HAVE_MMAP:

    class Mmap_backend(object):
        """
        Backend storage for our "array of bits" using an mmap'd file.

        Please note that this has only been tested on Linux so far: 2    -11-01.
        """

        effs = 2 ** 8 - 1

        def __init__(self, num_bits, filename):
            """Initialize."""
            self.num_bits = num_bits
            self.num_chars = (self.num_bits + 7) // 8
            flags = os.O_RDWR | os.O_CREAT
            if hasattr(os, 'O_BINARY'):
                flags |= getattr(os, 'O_BINARY')
            self.file_ = os.open(filename, flags)
            os.lseek(self.file_, self.num_chars + 1, os.SEEK_SET)
            os.write(self.file_, null_byte)
            self.mmap = mmap_mod.mmap(self.file_, self.num_chars)

        def is_set(self, bitno):
            """Return true iff bit number bitno is set."""
            byteno, bit_within_wordno = divmod(bitno, 8)
            mask = 1 << bit_within_wordno
            char = self.mmap[byteno]
            if isinstance(char, str):
                byte = ord(char)
            else:
                byte = int(char)
            return byte & mask

        def set(self, bitno):
            """Set bit number bitno to true."""
            byteno, bit_within_byteno = divmod(bitno, 8)
            mask = 1 << bit_within_byteno
            byte = self.mmap[byteno]
            byte |= mask
            self.mmap[byteno] = byte

        def clear(self, bitno):
            """Clear bit number bitno - set it to false."""
            byteno, bit_within_byteno = divmod(bitno, 8)
            mask = 1 << bit_within_byteno
            char = self.mmap[byteno]
            byte = ord(char)
            byte &= Mmap_backend.effs - mask
            self.mmap[byteno] = chr(byte)

        def __iand__(self, other):
            """Boolean "and" two bit arrays."""
            assert self.num_bits == other.num_bits

            for byteno in range(self.num_chars):
                self.mmap[byteno] = self.mmap[byteno] & other.mmap[byteno]

            return self

        def __ior__(self, other):
            """Boolean "or" two bit arrays."""
            assert self.num_bits == other.num_bits

            for byteno in range(self.num_chars):
                self.mmap[byteno] = self.mmap[byteno] | other.mmap[byteno]

            return self

        def close(self):
            """Close the file."""
            os.close(self.file_)


class File_seek_backend(object):
    """Backend storage for our "array of bits" using a file in which we seek."""

    effs = 2 ** 8 - 1

    def __init__(self, num_bits, filename):
        """Initialize."""
        self.num_bits = num_bits
        self.num_chars = (self.num_bits + 7) // 8
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, 'O_BINARY'):
            flags |= getattr(os, 'O_BINARY')
        self.file_ = os.open(filename, flags)
        os.lseek(self.file_, self.num_chars + 1, os.SEEK_SET)
        os.write(self.file_, null_byte)

    def is_set(self, bitno):
        """Return true iff bit number bitno is set."""
        byteno, bit_within_wordno = divmod(bitno, 8)
        mask = 1 << bit_within_wordno
        os.lseek(self.file_, byteno, os.SEEK_SET)
        byte = os.read(self.file_, 1)[0]
        return byte & mask

    def set(self, bitno):
        """Set bit number bitno to true."""
        byteno, bit_within_byteno = divmod(bitno, 8)
        mask = 1 << bit_within_byteno
        os.lseek(self.file_, byteno, os.SEEK_SET)
        byte = os.read(self.file_, 1)[0]
        byte |= mask
        os.lseek(self.file_, byteno, os.SEEK_SET)
        os.write(self.file_, bytes([byte]))

    def clear(self, bitno):
        """Clear bit number bitno - set it to false."""
        byteno, bit_within_byteno = divmod(bitno, 8)
        mask = 1 << bit_within_byteno
        os.lseek(self.file_, byteno, os.SEEK_SET)
        byte = os.read(self.file_, 1)[0]
        byte &= File_seek_backend.effs - mask
        os.lseek(self.file_, byteno, os.SEEK_SET)
        char = bytes([byte])
        os.write(self.file_, char)

    # These are quite slow ways to do iand and ior, but they should work, and a faster version is going to take more time
    def __iand__(self, other):
        """Boolean "and" two bit arrays."""
        assert self.num_bits == other.num_bits

        for bitno in range(self.num_bits):
            if self.is_set(bitno) and other.is_set(bitno):
                self.set(bitno)
            else:
                self.clear(bitno)

        return self

    def __ior__(self, other):
        """Boolean "or" two bit arrays."""
        assert self.num_bits == other.num_bits

        for bitno in range(self.num_bits):
            if self.is_set(bitno) or other.is_set(bitno):
                self.set(bitno)
            else:
                self.clear(bitno)

        return self

    def close(self):
        """Close the file."""
        os.close(self.file_)


class Array_then_file_seek_backend(object):
    # pylint: disable=R0902
    # R0902: We kinda need a bunch of instance attributes
    """
    Backend storage for our "array of bits" using a python array of integers up to some maximum number of bytes...

    ...then spilling over to a file.  This is -not- a cache; we instead save the leftmost bits in RAM, and the
    rightmost bits (if necessary) in a file.  On open, we read from the file to RAM.  On close, we write from RAM
    to the file.
    """

    effs = 2 ** 8 - 1

    def __init__(self, num_bits, filename, max_bytes_in_memory):
        """Initialize."""
        self.num_bits = num_bits
        num_chars = (self.num_bits + 7) // 8
        self.filename = filename
        self.max_bytes_in_memory = max_bytes_in_memory
        self.bits_in_memory = min(num_bits, self.max_bytes_in_memory * 8)
        self.bits_in_file = max(self.num_bits - self.bits_in_memory, 0)
        self.bytes_in_memory = (self.bits_in_memory + 7) // 8
        self.bytes_in_file = (self.bits_in_file + 7) // 8

        self.array_ = array.array('B', [0]) * self.bytes_in_memory
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, 'O_BINARY'):
            flags |= getattr(os, 'O_BINARY')
        self.file_ = os.open(filename, flags)
        # Make sure the file is large enough.
        os.lseek(self.file_, num_chars + 1, os.SEEK_SET)
        os.write(self.file_, null_byte)

        os.lseek(self.file_, 0, os.SEEK_SET)
        offset = 0
        intended_block_len = 2 ** 17
        while True:
            if offset + intended_block_len < self.bytes_in_memory:
                block = os.read(self.file_, intended_block_len)
            elif offset < self.bytes_in_memory:
                if offset == 0:
                    remainder = min(self.bytes_in_memory, offset)
                else:
                    remainder = self.bytes_in_memory % offset
                block = os.read(self.file_, remainder)
            else:
                break
            for index_in_block, character in enumerate(block):
                self.array_[offset + index_in_block] = character
            offset += intended_block_len

    def is_set(self, bitno):
        """Return true iff bit number bitno is set."""
        byteno, bit_within_byteno = divmod(bitno, 8)
        mask = 1 << bit_within_byteno
        if byteno < self.bytes_in_memory:
            return self.array_[byteno] & mask
        else:
            os.lseek(self.file_, byteno, os.SEEK_SET)
            byte = os.read(self.file_, 1)[0]
            return byte & mask

    def set(self, bitno):
        """Set bit number bitno to true."""
        byteno, bit_within_byteno = divmod(bitno, 8)
        mask = 1 << bit_within_byteno
        if byteno < self.bytes_in_memory:
            self.array_[byteno] |= mask
        else:
            os.lseek(self.file_, byteno, os.SEEK_SET)
            byte = os.read(self.file_, 1)[0]
            os.lseek(self.file_, byteno, os.SEEK_SET)
            byte |= mask
            os.write(self.file_, bytes([byte]))

    two_to_the_8th = 2 ** 8

    def clear(self, bitno):
        """Clear bit number bitno - set it to false."""
        # We did 8 bit bytes either way.
        byteno, bit_within_byteno = divmod(bitno, 8)
        assert 0 <= bit_within_byteno <= 7, f"bit_within_byteno is {bit_within_byteno}"
        mask = self.effs - (1 << bit_within_byteno)
        assert 1 <= mask <= self.two_to_the_8th, f"\n2**8 is {hex(self.two_to_the_8th)}\nmask  is {hex(mask)}"
        if byteno < self.bytes_in_memory:
            self.array_[byteno] &= mask
        else:
            os.lseek(self.file_, byteno, os.SEEK_SET)
            byte = os.read(self.file_, 1)[0]
            byte &= mask
            os.lseek(self.file_, byteno, os.SEEK_SET)
            os.write(self.file_, bytes([byte]))

    # These are quite slow ways to do iand and ior, but they should work, and a faster version is going to take more time
    def __iand__(self, other):
        """Boolean "and" two bit arrays."""
        assert self.num_bits == other.num_bits

        for bitno in range(self.num_bits):
            if self.is_set(bitno) and other.is_set(bitno):
                self.set(bitno)
            else:
                self.clear(bitno)

        return self

    def __ior__(self, other):
        """Boolean "or" two bit arrays."""
        assert self.num_bits == other.num_bits

        for bitno in range(self.num_bits):
            if self.is_set(bitno) or other.is_set(bitno):
                self.set(bitno)
            else:
                self.clear(bitno)

        return self

    def close(self):
        """Write the in-memory portion to disk, leave the already-on-disk portion unchanged."""
        os.lseek(self.file_, 0, os.SEEK_SET)
        # This is terribly slow, but it should work
        for index in range(self.bytes_in_memory):
            os.write(self.file_, bytes([self.array_[index]]))

        os.close(self.file_)


class Array_backend(object):
    """Backend storage for our "array of bits" using a python array of integers."""

    # Note that this has now been split out into a bits_mod for the benefit of other projects.
    effs = 2 ** 64 - 1

    def __init__(self, num_bits):
        """Initialize."""
        self.num_bits = num_bits
        self.num_words = (self.num_bits + 31) // 32
        self.array_ = array.array('L', [0]) * self.num_words

    def is_set(self, bitno):
        """Return true iff bit number bitno is set."""
        wordno, bit_within_wordno = divmod(bitno, 32)
        mask = 1 << bit_within_wordno
        return self.array_[wordno] & mask

    def set(self, bitno):
        """Set bit number bitno to true."""
        wordno, bit_within_wordno = divmod(bitno, 32)
        mask = 1 << bit_within_wordno
        self.array_[wordno] |= mask

    def clear(self, bitno):
        """Clear bit number bitno - set it to false."""
        wordno, bit_within_wordno = divmod(bitno, 32)
        mask = Array_backend.effs - (1 << bit_within_wordno)
        self.array_[wordno] &= mask

    # It'd be nice to do __iand__ and __ior__ in a base class, but that'd be Much slower
    def __iand__(self, other):
        """Boolean "and" two bit arrays."""
        assert self.num_bits == other.num_bits

        for wordno in range(self.num_words):
            self.array_[wordno] &= other.array_[wordno]

        return self

    def __ior__(self, other):
        """Boolean "or" two bit arrays."""
        assert self.num_bits == other.num_bits

        for wordno in range(self.num_words):
            self.array_[wordno] |= other.array_[wordno]

        return self

    def close(self):
        """Noop for compatibility with the file+seek backend."""
        pass


def get_bitno_seed_rnd(bloom_filter, key):
    """Apply num_probes_k hash functions to key.  Generate the array index and bitmask corresponding to each result."""
    # We're using key as a seed to a pseudorandom number generator
    hasher = random.Random(key).randrange
    for _unused in range(bloom_filter.num_probes_k):
        bitno = hasher(bloom_filter.num_bits_m)
        yield bitno % bloom_filter.num_bits_m


MERSENNES1 = [2 ** x - 1 for x in [17, 31, 127]]
MERSENNES2 = [2 ** x - 1 for x in [19, 67, 257]]


def simple_hash(int_list, prime1, prime2, prime3):
    """Compute a hash value from a list of integers and 3 primes."""
    result = 0
    for integer in int_list:
        result += ((result + integer + prime1) * prime2) % prime3
    return result


def hash1(int_list):
    """Hash input: function #1."""
    return simple_hash(int_list, MERSENNES1[0], MERSENNES1[1], MERSENNES1[2])


def hash2(int_list):
    """Hash input: function #2."""
    return simple_hash(int_list, MERSENNES2[0], MERSENNES2[1], MERSENNES2[2])


def get_bitno_lin_comb(bloom_filter, key):
    """Apply num_probes_k hash functions to key.  Generate the array index and bitmask corresponding to each result."""
    # This one assumes key is either bytes or str (or other list of integers)

    # I'd love to check for long too, but that doesn't exist in 3.2, and 2.5 doesn't have the numbers.Integral base type
    if hasattr(key, '__divmod__'):
        int_list = []
        temp = key
        while temp:
            quotient, remainder = divmod(temp, 256)
            int_list.append(remainder)
            temp = quotient
    elif hasattr(key[0], '__divmod__'):
        int_list = key
    elif isinstance(key[0], str):
        int_list = [ord(char) for char in key]
    else:
        raise TypeError('Sorry, I do not know how to hash this type')

    hash_value1 = hash1(int_list)
    hash_value2 = hash2(int_list)

    # We're using linear combinations of hash_value1 and hash_value2 to obtain num_probes_k hash functions
    for probeno in range(1, bloom_filter.num_probes_k + 1):
        bit_index = hash_value1 + probeno * hash_value2
        yield bit_index % bloom_filter.num_bits_m


def try_unlink(filename):
    """Delete a file.  Don't complain if it's not there."""
    try:
        os.unlink(filename)
    except OSError:
        pass
    return


class Bloom_filter(object):
    """Probabilistic set membership testing for large sets."""

    def __init__(self, ideal_num_elements_n, error_rate_p, probe_bitnoer=get_bitno_lin_comb, filename=None, start_fresh=False):
        """
        Initialize.

        If filename is None: use an in-memory array.
        If filename is a tuple and the second element is an int:
            The first element will be treated as a filename in the filesystem.
            If the second element's value is -1: use mmap for the whole file.
            If the second element's value is any other int: use an in-memory array for the beginning of the filter, then switch
                to file seek if too many elements are needed.
        If the filename is not None and not a tuple, treat it as a filename and use file-seek for the entire datastructure.
        """
        # pylint: disable=R0913
        # R0913: We want a few arguments
        if ideal_num_elements_n <= 0:
            raise ValueError('ideal_num_elements_n must be > 0')
        if not (0 < error_rate_p < 1):
            raise ValueError('error_rate_p must be between 0 and 1 exclusive')

        self.error_rate_p = error_rate_p
        # With fewer elements, we should do very well.  With more elements, our error rate "guarantee"
        # drops rapidly.
        self.ideal_num_elements_n = ideal_num_elements_n

        numerator = -1 * self.ideal_num_elements_n * math.log(self.error_rate_p)
        denominator = math.log(2) ** 2
        real_num_bits_m = numerator / denominator
        self.num_bits_m = int(math.ceil(real_num_bits_m))

        if filename is None:
            self.backend = Array_backend(self.num_bits_m)
        elif isinstance(filename, tuple) and isinstance(filename[1], int):
            if start_fresh:
                try_unlink(filename[0])
            if filename[1] == -1:
                self.backend = Mmap_backend(self.num_bits_m, filename[0])
            else:
                self.backend = Array_then_file_seek_backend(self.num_bits_m, filename=filename[0], max_bytes_in_memory=filename[1])
        else:
            if start_fresh:
                try_unlink(filename)
            self.backend = File_seek_backend(self.num_bits_m, filename)

        # AKA num_offsetters
        # Verified against http://en.wikipedia.org/wiki/Bloom_filter#Probability_of_false_positives
        real_num_probes_k = (self.num_bits_m / self.ideal_num_elements_n) * math.log(2)
        self.num_probes_k = int(math.ceil(real_num_probes_k))

# This comes close, but often isn't the same value
#        alternative_real_num_probes_k = -math.log(self.error_rate_p) / math.log(2)
#
#        if abs(real_num_probes_k - alternative_real_num_probes_k) > 1e-6:
#            sys.stderr.write('real_num_probes_k: %f, alternative_real_num_probes_k: %f\n' %
#                (real_num_probes_k, alternative_real_num_probes_k)
#                )
#            sys.exit(1)

        self.probe_bitnoer = probe_bitnoer

    def __repr__(self):
        """Convert to string representation."""
        return 'Bloom_filter(ideal_num_elements_n=%d, error_rate_p=%f, num_bits_m=%d)' % (
            self.ideal_num_elements_n,
            self.error_rate_p,
            self.num_bits_m,
        )

    def add(self, key):
        """Add an element to the filter."""
        for bitno in self.probe_bitnoer(self, key):
            self.backend.set(bitno)

    def __iadd__(self, key):
        """Add key to the filter."""
        self.add(key)
        return self

    def _match_template(self, other):
        """Compare a sort of signature for two bloom filters.  Used in preparation for binary operations."""
        return (self.num_bits_m == other.num_bits_m and
                self.num_probes_k == other.num_probes_k and
                self.probe_bitnoer == other.probe_bitnoer)

    def union(self, other):
        """Compute the set union of two bloom filters."""
        self.backend |= other.backend

    def __ior__(self, other):
        """Compute the set union of two bloom filters."""
        self.union(other)
        return self

    def intersection(self, other):
        """Compute the set intersection of two bloom filters."""
        self.backend &= other.backend

    def __iand__(self, other):
        """Compute the set intersection of two bloom filters."""
        self.intersection(other)
        return self

    def __contains__(self, key):
        """Check if key is probably in the filter."""
        for bitno in self.probe_bitnoer(self, key):
            if not self.backend.is_set(bitno):
                return False
        return True

    def close(self):
        """Close the file, if any."""
        self.backend.close()
