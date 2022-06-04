import resource


MAX_MEM = 512*1024*1024
resource.setrlimit(resource.RLIMIT_AS, (MAX_MEM, MAX_MEM))

mem_limit = resource.getrlimit(resource.RLIMIT_AS)

print(mem_limit)