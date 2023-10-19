import time
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    time0 = time.time()
    with open('./artifacts/log.txt', mode='w') as f:
        f.write('%.2f sec OK'%(time.time()-time0))
