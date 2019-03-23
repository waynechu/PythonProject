import dns.zone

zone = dns.zone.from_file("D:\\Workspace\\GitHub\\PythonProject\\testdev.com.zone", origin="testdev.com")
for (name, ttl, rdata) in zone.iterate_rdatas():
    print(name.to_text(), ttl, rdata.extended_rdatatype(), rdata.to_text())
print("")
print(zone.to_text())