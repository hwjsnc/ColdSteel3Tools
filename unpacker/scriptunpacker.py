import os, json

def unpack(path=None, projectName=None):
    os.makedirs(f'projects/{projectName}/scripts', exist_ok=True)
    scriptTypes = ['scena', 'talk']

    for scriptType in scriptTypes:
        outpath = f'projects/{projectName}/scripts/{scriptType}'
        os.makedirs(outpath, exist_ok=True)
        scriptPath = f'{path}/data/scripts/{scriptType}/dat_en'
        files = [f.name for f in os.scandir(scriptPath) if f.is_file()]
        for file in files:
            os.makedirs(f'{outpath}/{file}', exist_ok=True)
            with open(f'{scriptPath}/{file}', 'rb') as scriptFile, open(f'{outpath}/{file}/summary.json', 'w') as summaryFile:
                summary = {}
                scriptFile.read(8)
                startLocation = int.from_bytes(scriptFile.read(4), 'little')
                scriptFile.read(8)
                entryNum = int.from_bytes(scriptFile.read(4), 'little')
                headerEnd = int.from_bytes(scriptFile.read(4), 'little')

                scriptFile.seek(startLocation)
                actualStart = int.from_bytes(scriptFile.read(4), 'little')
                summary['diff'] = actualStart - headerEnd
                summary['names'] = list()

                scriptFile.seek(startLocation)

                dataLocation = []
                entryNameLocation = []
                entryName = []

                for i in range(entryNum):
                    dataLocation.append(int.from_bytes(scriptFile.read(4), 'little'))

                for i in range(entryNum):
                    entryNameLocation.append(int.from_bytes(scriptFile.read(2), 'little'))
                nameLocationStart = scriptFile.tell()
                names = scriptFile.read(headerEnd - nameLocationStart - 1)
                entryName = [name.decode('utf-8') for name in names.split(b'\x00')]
                for i in range(entryNum):
                    summary['names'].append({f'{entryNameLocation[i]}' : f'{entryName[i]}'})
                json.dump(summary, summaryFile, indent='\t')
                
                if len(entryName) == 1 and entryName[0] == '':
                    continue

                order = 0
                for i in range(entryNum - 1):
                    with open(f'{outpath}/{file}/{order}.{entryName[i]}', 'wb') as dataFile:
                        scriptFile.seek(dataLocation[i])
                        dataFile.write(scriptFile.read(dataLocation[i+1] - dataLocation[i]))
                    order += 1
                
                with open(f'{outpath}/{file}/{order}.{entryName[entryNum - 1]}', 'wb') as dataFile:
                    scriptFile.seek(dataLocation[entryNum - 1])
                    dataFile.write(scriptFile.read())