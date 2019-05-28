
### on Mac
quicdir = "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicPLT/"

def writeToFile(path, data):
    with open(path, 'a') as f:
        f.write("%s" %data)

if __name__ == "__main__":
    data="1 2 3 4\n5 6 7 8\n"
    writeToFile(quicdir+"test.txt",data)
    writeToFile(quicdir+"test.txt",data)
    writeToFile(quicdir+"test.txt",data)