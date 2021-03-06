#
# Convert a hexa string (from a LDIF export) to an UTF8 string
#
function hextostr
{
    Param([STRING] $inStr)

    $s = $inStr -match "^X'(.+)'$"

    if ($s)
    {
        $Encode = new-object 'System.Text.UTF8Encoding'
        $outStr = $encode.getstring(($matches[1]  -split '(..)' | ? { $_ } | % {[BYTE]([CONVERT]::toint16($_,16)) }))
    }
    return $outStr
}

$str = "X'53C3A96261737469656E'"

$str=hextostr $str
echo $str