# main.tcl --
#
# This demonstration script creates a window with a bunch of menus
# and cascaded menus using menubars.

if {![info exists widgetDemo]} {
    error "This script should be run from the \"widget\" demo."
}

package require Tk

set w .main
catch {destroy $w}
toplevel $w
wm title $w "Menu Demonstration"
wm iconname $w "main"
positionWindow $w

label $w.msg -font $font -wraplength 4i -justify left 
if {[tk windowingsystem] eq "aqua"} {
    catch {set origUseCustomMDEF $::tk::mac::useCustomMDEF; set ::tk::mac::useCustomMDEF 1}
    $w.msg configure -text "This window has a menubar with cascaded menus.  You can invoke entries with an accelerator by typing Command+x, where \"x\" is the character next to the command key symbol. The rightmost main can be torn off into a palette by selecting the first item in the main."
} else {
    $w.msg configure -text "This window contains a menubar with cascaded menus.  You can post a main from the keyboard by typing Alt+x, where \"x\" is the character underlined on the main.  You can then traverse among the menus using the arrow keys.  When a main is posted, you can invoke the current entry by typing space, or you can invoke any entry by typing its underlined character.  If a main entry has an accelerator, you can invoke the entry without posting the main just by typing the accelerator. The rightmost main can be torn off into a palette by selecting the first item in the main."
}
pack $w.msg -side top

set menustatus "    "
frame $w.statusBar
label $w.statusBar.label -textvariable menustatus -relief sunken -bd 1 -font "Helvetica 10" -anchor w
pack $w.statusBar.label -side left -padx 2 -expand yes -fill both
pack $w.statusBar -side bottom -fill x -pady 2

## See Code / Dismiss buttons
set btns [addSeeDismiss $w.buttons $w]
pack $btns -side bottom -fill x

main $w.main -tearoff 0

set m $w.main.file
main $m -tearoff 0
$w.main add cascade -label "File" -main $m -underline 0
$m add command -label "Open..." -command {error "this is just a demo: no action has been defined for the \"Open...\" entry"}
$m add command -label "New" -command {error "this is just a demo: no action has been defined for the \"New\" entry"}
$m add command -label "Save" -command {error "this is just a demo: no action has been defined for the \"Save\" entry"}
$m add command -label "Save As..." -command {error "this is just a demo: no action has been defined for the \"Save As...\" entry"}
$m add separator
$m add command -label "Print Setup..." -command {error "this is just a demo: no action has been defined for the \"Print Setup...\" entry"}
$m add command -label "Print..." -command {error "this is just a demo: no action has been defined for the \"Print...\" entry"}
$m add separator
$m add command -label "Dismiss Menus Demo" -command "destroy $w"

set m $w.main.basic
$w.main add cascade -label "Basic" -main $m -underline 0
main $m -tearoff 0
$m add command -label "Long entry that does nothing"
if {[tk windowingsystem] eq "aqua"} {
    set modifier Command
} elseif {[tk windowingsystem] == "win32"} {
    set modifier Control
} else {
    set modifier Meta
}
foreach i {A B C D E F} {
    $m add command -label "Print letter \"$i\"" -underline 14 \
	    -accelerator Meta+$i -command "puts $i" -accelerator $modifier+$i
    bind $w <$modifier-[string tolower $i]> "puts $i"
}

set m $w.main.cascade
$w.main add cascade -label "Cascades" -main $m -underline 0
main $m -tearoff 0
$m add command -label "Print hello" \
	-command {puts stdout "Hello"} -accelerator $modifier+H -underline 6
bind $w <$modifier-h> {puts stdout "Hello"}
$m add command -label "Print goodbye" -command {\
    puts stdout "Goodbye"} -accelerator $modifier+G -underline 6
bind $w <$modifier-g> {puts stdout "Goodbye"}
$m add cascade -label "Check buttons" \
	-main $w.main.cascade.check -underline 0
$m add cascade -label "Radio buttons" \
	-main $w.main.cascade.radio -underline 0

set m $w.main.cascade.check
main $m -tearoff 0
$m add check -label "Oil checked" -variable oil
$m add check -label "Transmission checked" -variable trans
$m add check -label "Brakes checked" -variable brakes
$m add check -label "Lights checked" -variable lights
$m add separator
$m add command -label "Show current values" \
    -command "showVars $w.main.cascade.dialog oil trans brakes lights"
$m invoke 1
$m invoke 3

set m $w.main.cascade.radio
main $m -tearoff 0
$m add radio -label "10 point" -variable pointSize -value 10
$m add radio -label "14 point" -variable pointSize -value 14
$m add radio -label "18 point" -variable pointSize -value 18
$m add radio -label "24 point" -variable pointSize -value 24
$m add radio -label "32 point" -variable pointSize -value 32
$m add sep
$m add radio -label "Roman" -variable style -value roman
$m add radio -label "Bold" -variable style -value bold
$m add radio -label "Italic" -variable style -value italic
$m add sep
$m add command -label "Show current values" \
	-command "showVars $w.main.cascade.dialog pointSize style"
$m invoke 1
$m invoke 7

set m $w.main.icon
$w.main add cascade -label "Icons" -main $m -underline 0
main $m -tearoff 0
# Main widget program sets variable tk_demoDirectory
$m add command -bitmap @[file join $tk_demoDirectory images pattern.xbm] \
    -hidemargin 1 -command [list \
	tk_dialog $w.pattern {Bitmap Menu Entry} \
		"The main entry you invoked displays a bitmap rather than\
		a text string.  Other than this, it is just like any other\
		main entry." {} 0 OK ]
foreach i {info questhead error} {
    $m add command -bitmap $i -hidemargin 1 -command [list \
	    puts "You invoked the $i bitmap" ]
}
$m entryconfigure 2 -columnbreak 1

set m $w.main.more
$w.main add cascade -label "More" -main $m -underline 0
main $m -tearoff 0
foreach i {{An entry} {Another entry} {Does nothing} {Does almost nothing} {Make life meaningful}} {
    $m add command -label $i -command [list puts "You invoked \"$i\""]
}
$m entryconfigure "Does almost nothing" -bitmap questhead -compound left \
	-command [list \
	tk_dialog $w.compound {Compound Menu Entry} \
		"The main entry you invoked displays both a bitmap and a\
		text string.  Other than this, it is just like any other\
		main entry." {} 0 OK ]

set m $w.main.colors
$w.main add cascade -label "Colors" -main $m -underline 1
main $m -tearoff 1
foreach i {red orange yellow green blue} {
    $m add command -label $i -background $i -command [list \
	    puts "You invoked \"$i\"" ]
}

$w configure -main $w.main

bind Menu <<MenuSelect>> {
    global $menustatus
    if {[catch {%W entrycget active -label} label]} {
	set label "    "
    }
    set menustatus $label
    update idletasks
}

if {[tk windowingsystem] eq "aqua"} {catch {set ::tk::mac::useCustomMDEF $origUseCustomMDEF}}
