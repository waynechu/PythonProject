import dns.zone

zone = dns.zone.from_file("D:\\Workspace\\GitHub\\PythonProject\\testdev.com.zone", origin="testdev.com")
for (name, ttl, rdata) in zone.iterate_rdatas():
    print(type(name), type(ttl), type(rdata))
    print(name, ttl, rdata)
print(zone.to_text())