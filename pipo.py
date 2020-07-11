from typing import List
import os


############### LIB PATH ###############
lib_path = "./lib"

# Select pip, pip3, pip36, pip38 etc.
which_pip = input("Which pip >>> ")

try:
    # Change Dir to this file path.
    os.chdir(os.path.dirname( __file__ ))

except:
    pass

if ( not os.path.exists( lib_path ) ):
    os.mkdir( lib_path )

###################################################################################

# get all package files by name.
def search_files( _string: str, _list_of_str: List[str] ):
    """ Search A String In A List Of String """
    result = []
    for pFile in _list_of_str:
        if _string.lower().replace('-', '_') in pFile.lower():# and '.whl' in pFile:
            result.append(pFile)
    return result


#####################################################################################

def parse_version(version):
    ver = version.split('.')
    return int(ver[0] + ver[1] + ver[2])


#####################################################################################


# Parse Package Files. as = {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
def parse_package(pFiles):
    packages = {}
    # Loop Through All Versions
    for pFile in pFiles:
        # Extrect Filename & Extention.
        file_name, _ext = pFile.split('.whl')
        # Extrect Info ModuleName, Version, OtherInfo.
        info = file_name.split('-', 2)
        if len(info) == 3:
            package = { 'name': info[0],'ver': info[1], 'others':info[2], 'fname':pFile }
            if info[2] in packages:
                packages[info[2]].append(package)
            else:
                packages[info[2]] = [package]

    return packages


#####################################################################################
    

def get_older_versions(_packages, _delete = False):
    """ If Same Version  Found Then Delete Older Versions """
    result = []
    for key in _packages.keys():
        if len(_packages[key]) > 1:
            # Reverse Sort By Version.
            _packages[key].sort(key=lambda p:parse_version(p['ver']) , reverse=True)
            # Keep Leatest Version and Loop over older version.
            for package in _packages[key][1:]:
                result.append(package)
                if _delete:
                    os.remove(os.path.join( lib_path, package['fname'] ))
                        
    return result



################################### Massy Codes ##########################################


def main():
    package_name = input('Enter Package Name >>> ')
    if package_name == '':
        return
    elif package_name.lower() == 'exit':
        quit()
    package_files = search_files( package_name, os.listdir( lib_path ))
    packages = parse_package(package_files)
    
    for key in packages.keys():
        if len(packages[key]) == 1:
            print(key + " -> " + packages[key][0]['ver'] )
        else:
            print(key)
            for package in packages[key]:
                ver = package['ver']
                print(f'\t -> { ver }')
    print( '\n\nCommands: \'Download\', \'Clean\', \'Install\', \'exit\' ' )
    ui = input('>>> ')
    
    # Check User Input And Trigger Action.
    if ui.lower() == 'clean':
        older_versions = get_older_versions(packages, True)
        if len(older_versions) == 0:
            input('No Older Version To Clean...')
    elif ui.lower() == 'download':
        os.system(which_pip + ' download ' + package_name + ' -d ' + lib_path)
        if len(package_files) == 0:
            r = input('Add To List ? \'y\'/\'n\' >>> ')
            if r.lower() == 'y':
                desc = input('\n\nEnter Some Description About This Module\n>>> ')
                with open('modules.txt', 'a') as fl:
                    fl.write(f'\n{package_name} - {desc}')
                    fl.close()
                
        
        input('...')
    elif ui.lower() == 'install':
        os.system(which_pip + ' install ' + package_name + ' --no-index --find-links ' + lib_path )
        input('...')
    elif ui.lower() == 'exit':
        quit()
    

# If This Is Luncher Then Clean Older Version
if __name__ == '__main__':
    while True:
        os.system('cls')
        main()
