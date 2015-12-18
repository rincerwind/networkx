
'''
The murmurHash3 function as described by Thomas Pajor
in https://github.com/Luftschlange/ms-skim/blob/master/src/SKIM.h
'''
def murmurHash3(u,v,i,l, randomSeed):
    randomSeed &= 0xFFFFFFFF
    h = (randomSeed<<16)+l
    
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # Hash the first vertex
    k = u
    k = (c1 * k)
    k = rol(k, 15, 32)
    k = ( c2 * k )
    h ^= k
    h = rol(h, 13, 32)
    h = ( h * 5 + 0xe6546b64 )

    # Hash the second vertex
    k = v
    k = (c1 * k)
    k = rol(k, 15, 32)
    k = ( c2 * k )
    h ^= k
    h = rol(h, 13, 32)
    h = ( h * 5 + 0xe6546b64 )

    # Hash the instance
    k = i
    k = (c1 * k)
    k = rol(k, 15, 32)
    k = ( c2 * k )
    h ^= k

    # Mix the results
    h ^= 10
    h ^= (h >> 16)
    h = ( h * 0x85ebca6b )
    h ^= (h >> 13)
    h = ( h * 0xc2b2ae35 ) 
    h ^= (h >> 16)
    
    return h

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))