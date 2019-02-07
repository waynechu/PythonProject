from pyssdb import pyssdb


if __name__ == '__main__':
    ConfSSDB = pyssdb.Client(host = "104.199.145.233", port = 4001)

    ConfSSDB.auth("sa23891odi1@8hfn!0932aqiomc9AQjiHH")

    #print(ConfSSDB.hgetall("DNS-Agent-Sync"), end = "\n\n")
    #print(ConfSSDB.hkeys("DNS-Agent-Sync", "", "", 100), end = "\n\n")
    #print(ConfSSDB.hgetall("DNS-Agent-Status"), end = "\n\n")
    #print(ConfSSDB.hkeys("DNS-Agent-Status", "", "", 100), end = "\n\n")

    Names = ConfSSDB.hlist("", "", 100)

    for Name in Names:
        print(Name)

    print("------------------------------")

    LogSize = ConfSSDB.hsize("DNS-Agent-Log-HKSGDNSDF01")
    hksgdnsdf01 = ConfSSDB.hgetall("DNS-Agent-Log-HKSGDNSDF01", "", "", LogSize)
    for log in hksgdnsdf01:
        print(log)

    print("------------------------------")

    StatusSize = ConfSSDB.hsize("DNS-Agent-Sync")
    StatusHashes = ConfSSDB.hkeys("DNS-Agent-Sync", "", "", StatusSize)

    for Agent in StatusHashes:
        Status = ConfSSDB.hget("DNS-Agent-Sync", Agent)
        if Status == b"Sync":
            print(Agent, "is good!")
        else:
            print(Agent, "in trouble!")

    ConfSSDB.disconnect()