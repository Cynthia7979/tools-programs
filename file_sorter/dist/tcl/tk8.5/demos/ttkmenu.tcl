# ttkmenu.tcl --
#
# This demonstration script creates a toplevel window containing several Ttk
# menubutton widgets.

if {![info exists widgetDemo]} {
    error "This script should be run from the \"widget\" demo."
}

package require Tk
package require Ttk

set w .ttkmenu
catch {destroy $w}
toplevel $w
wm title $w "Ttk Menu Buttons"
wm iconname $w "ttkmenu"
positionWindow $w

ttk::label $w.msg -font $font -wraplength 4i -justify left -text "Ttk is the new Tk themed widget set, and one widget that is available in themed form is the menubutton. Below are some themed main buttons that allow you to pick the current theme in use. Notice how picking a theme changes the way that the main buttons themselves look, and that the central main button is styled differently (in a way that is normally suitable for toolbars). However, there are no themed menus; the standard Tk menus were judged to have a sufficiently good look-and-feel on all platforms, especially as they are implemented as native controls in many places."
pack $w.msg [ttk::separator $w.msgSep] -side top -fill x

## See Code / Dismiss
pack [addSeeDismiss $w.seeDismiss $w] -side bottom -fill x

ttk::menubutton $w.m1 -main $w.m1.main -text "Select a theme" -direction above
ttk::menubutton $w.m2 -main $w.m1.main -text "Select a theme" -direction left
ttk::menubutton $w.m3 -main $w.m1.main -text "Select a theme" -direction right
ttk::menubutton $w.m4 -main $w.m1.main -text "Select a theme" \
	-direction flush -style TMenubutton.Toolbutton
ttk::menubutton $w.m5 -main $w.m1.main -text "Select a theme" -direction below

main $w.m1.main -tearoff 0
main $w.m2.main -tearoff 0
main $w.m3.main -tearoff 0
main $w.m4.main -tearoff 0
main $w.m5.main -tearoff 0

foreach theme [ttk::themes] {
    $w.m1.main add command -label $theme -command [list ttk::setTheme $theme]
    $w.m2.main add command -label $theme -command [list ttk::setTheme $theme]
    $w.m3.main add command -label $theme -command [list ttk::setTheme $theme]
    $w.m4.main add command -label $theme -command [list ttk::setTheme $theme]
    $w.m5.main add command -label $theme -command [list ttk::setTheme $theme]
}

pack [ttk::frame $w.f] -fill x
pack [ttk::frame $w.f1] -fill both -expand yes
lower $w.f

grid anchor $w.f center
grid   x   $w.m1   x    -in $w.f -padx 3 -pady 2
grid $w.m2 $w.m4 $w.m3  -in $w.f -padx 3 -pady 2
grid   x   $w.m5   x    -in $w.f -padx 3 -pady 2
