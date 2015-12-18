
'''
The murmurHash3 function as described by Thomas Pajor
in https://github.com/Luftschlange/ms-skim/blob/master/src/SKIM.h
'''
def murmurHash3(u,v,i,l, randomSeed):
    h = (randomSeed<<16)+l
    
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # Hash the first vertex
    k = u
    k = (c1 * k) & 0xFFFFFFFF
    k = ( k << 15 | k >> 17 ) & 0xFFFFFFFF # inline rotl
    k = ( c2 * k ) & 0xFFFFFFFF
    h ^= k
    h = ( h << 13 | h >> 19 ) & 0xFFFFFFFF # inline rotl
    h = ( h * 5 + 0xe6546b64 ) & 0xFFFFFFFF

    # Hash the second vertex
    k = v
    k = (c1 * k) & 0xFFFFFFFF
    k = ( k << 15 | k >> 17 ) & 0xFFFFFFFF # inline rotl
    k = ( c2 * k ) & 0xFFFFFFFF
    h ^= k
    h = ( h << 13 | h >> 19 ) & 0xFFFFFFFF # inline rotl
    h = ( h * 5 + 0xe6546b64 ) & 0xFFFFFFFF

    # Hash the instance
    k = i
    k = (c1 * k) & 0xFFFFFFFF
    k = ( k << 15 | k >> 17 ) & 0xFFFFFFFF # inline rotl
    k = ( c2 * k ) & 0xFFFFFFFF
    h ^= k

    # Mix the results
    h ^= 10
    h ^= (h >> 16)
    h = ( h * 0x85ebca6b ) & 0xFFFFFFFF
    h ^= (h >> 13)
    h = ( h * 0xc2b2ae35 ) & 0xFFFFFFFF
    h ^= (h >> 16)
    
    return h