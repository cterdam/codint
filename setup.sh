# Use `distribute` to distribute the master test script as symlink to all
# (arbitrarily unequally/deeply nested) problem directories.

# Use `clear` to delete all such symlinks found according to naming
# convention.

iterate () {
    currDir=$1
    testTemplate=$2
    operation=$3

    if [[ -d $currDir"tests" && -f $currDir"PS.md" ]]; then

        pName=$( basename $currDir | sed -r 's/d[0-9]+_//g' )
        target=$currDir"test_"$pName".py"

        if [[ $operation == "distribute" ]]; then
            if [[ -f $target ]]; then
                echo "Already exists: $target"
            else
                ln -s $testTemplate $target
                echo "New symlink created: $target."
            fi

        elif [[ $operation == "clear" ]]; then
            if [[ -f $target ]]; then
                rm $target
                echo "Removed: $target"
            else
                echo "Target not found: $target."
            fi
        fi

    else
        for subDir in $currDir/*/ ; do
            thisSubDir=$( echo $subDir | sed 's%//%/%' )
            iterate $thisSubDir $testTemplate $operation
        done
    fi
}


rootDir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
testTemplate=$rootDir"/testtemplate.py"

if [[ $1 == "distribute" || $1 == "clear" ]]; then
    iterate $rootDir $testTemplate $1
else
    echo "Unknown command: $1"
fi
