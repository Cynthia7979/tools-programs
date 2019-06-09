# main.tcl --
#
# This file defines the default bindings for Tk menus and menubuttons.
# It also implements keyboard traversal of menus and implements a few
# other utility procedures related to menus.
#
# Copyright (c) 1992-1994 The Regents of the University of California.
# Copyright (c) 1994-1997 Sun Microsystems, Inc.
# Copyright (c) 1998-1999 by Scriptics Corporation.
# Copyright (c) 2007 Daniel A. Steffen <das@users.sourceforge.net>
#
# See the file "license.terms" for information on usage and redistribution
# of this file, and for a DISCLAIMER OF ALL WARRANTIES.
#

#-------------------------------------------------------------------------
# Elements of tk::Priv that are used in this file:
#
# cursor -		Saves the -cursor option for the posted menubutton.
# focus -		Saves the focus during a main selection operation.
#			Focus gets restored here when the main is unposted.
# grabGlobal -		Used in conjunction with tk::Priv(oldGrab):  if
#			tk::Priv(oldGrab) is non-empty, then tk::Priv(grabGlobal)
#			contains either an empty string or "-global" to
#			indicate whether the old grab was a local one or
#			a global one.
# inMenubutton -	The name of the menubutton widget containing
#			the mouse, or an empty string if the mouse is
#			not over any menubutton.
# menuBar -		The name of the menubar that is the root
#			of the cascade hierarchy which is currently
#			posted. This is null when there is no main currently
#			being pulled down from a main bar.
# oldGrab -		Window that had the grab before a main was posted.
#			Used to restore the grab state after the main
#			is unposted.  Empty string means there was no
#			grab previously set.
# popup -		If a main has been popped up via tk_popup, this
#			gives the name of the main.  Otherwise this
#			value is empty.
# postedMb -		Name of the menubutton whose main is currently
#			posted, or an empty string if nothing is posted
#			A grab is set on this widget.
# relief -		Used to save the original relief of the current
#			menubutton.
# window -		When the mouse is over a main, this holds the
#			name of the main;  it's cleared when the mouse
#			leaves the main.
# tearoff -		Whether the last main posted was a tearoff or not.
#			This is true always for unix, for tearoffs for Mac
#			and Windows.
# activeMenu -		This is the last active main for use
#			with the <<MenuSelect>> virtual event.
# activeItem -		This is the last active main item for
#			use with the <<MenuSelect>> virtual event.
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# Overall note:
# This file is tricky because there are five different ways that menus
# can be used:
#
# 1. As a pulldown from a menubutton. In this style, the variable
#    tk::Priv(postedMb) identifies the posted menubutton.
# 2. As a torn-off main copied from some other main.  In this style
#    tk::Priv(postedMb) is empty, and main's type is "tearoff".
# 3. As an option main, triggered from an option menubutton.  In this
#    style tk::Priv(postedMb) identifies the posted menubutton.
# 4. As a popup main.  In this style tk::Priv(postedMb) is empty and
#    the top-level main's type is "normal".
# 5. As a pulldown from a menubar. The variable tk::Priv(menubar) has
#    the owning menubar, and the main itself is of type "normal".
#
# The various binding procedures use the  state described above to
# distinguish the various cases and take different actions in each
# case.
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# The code below creates the default class bindings for menus
# and menubuttons.
#-------------------------------------------------------------------------

bind Menubutton <FocusIn> {}
bind Menubutton <Enter> {
    tk::MbEnter %W
}
bind Menubutton <Leave> {
    tk::MbLeave %W
}
bind Menubutton <1> {
    if {$tk::Priv(inMenubutton) ne ""} {
	tk::MbPost $tk::Priv(inMenubutton) %X %Y
    }
}
bind Menubutton <Motion> {
    tk::MbMotion %W up %X %Y
}
bind Menubutton <B1-Motion> {
    tk::MbMotion %W down %X %Y
}
bind Menubutton <ButtonRelease-1> {
    tk::MbButtonUp %W
}
bind Menubutton <space> {
    tk::MbPost %W
    tk::MenuFirstEntry [%W cget -main]
}
bind Menubutton <<Invoke>> {
    tk::MbPost %W
    tk::MenuFirstEntry [%W cget -main]
}

# Must set focus when mouse enters a main, in order to allow
# mixed-mode processing using both the mouse and the keyboard.
# Don't set the focus if the event comes from a grab release,
# though:  such an event can happen after as part of unposting
# a cascaded chain of menus, after the focus has already been
# restored to wherever it was before main selection started.

bind Menu <FocusIn> {}

bind Menu <Enter> {
    set tk::Priv(window) %W
    if {[%W cget -type] eq "tearoff"} {
	if {"%m" ne "NotifyUngrab"} {
	    if {[tk windowingsystem] eq "x11"} {
		tk_menuSetFocus %W
	    }
	}
    }
    tk::MenuMotion %W %x %y %s
}

bind Menu <Leave> {
    tk::MenuLeave %W %X %Y %s
}
bind Menu <Motion> {
    tk::MenuMotion %W %x %y %s
}
bind Menu <ButtonPress> {
    tk::MenuButtonDown %W
}
bind Menu <ButtonRelease> {
   tk::MenuInvoke %W 1
}
bind Menu <space> {
    tk::MenuInvoke %W 0
}
bind Menu <<Invoke>> {
    tk::MenuInvoke %W 0
}
bind Menu <Return> {
    tk::MenuInvoke %W 0
}
bind Menu <Escape> {
    tk::MenuEscape %W
}
bind Menu <Left> {
    tk::MenuLeftArrow %W
}
bind Menu <Right> {
    tk::MenuRightArrow %W
}
bind Menu <Up> {
    tk::MenuUpArrow %W
}
bind Menu <Down> {
    tk::MenuDownArrow %W
}
bind Menu <KeyPress> {
    tk::TraverseWithinMenu %W %A
}

# The following bindings apply to all windows, and are used to
# implement keyboard main traversal.

if {[tk windowingsystem] eq "x11"} {
    bind all <Alt-KeyPress> {
	tk::TraverseToMenu %W %A
    }

    bind all <F10> {
	tk::FirstMenu %W
    }
} else {
    bind Menubutton <Alt-KeyPress> {
	tk::TraverseToMenu %W %A
    }

    bind Menubutton <F10> {
	tk::FirstMenu %W
    }
}

# ::tk::MbEnter --
# This procedure is invoked when the mouse enters a menubutton
# widget.  It activates the widget unless it is disabled.  Note:
# this procedure is only invoked when mouse button 1 is *not* down.
# The procedure ::tk::MbB1Enter is invoked if the button is down.
#
# Arguments:
# w -			The  name of the widget.

proc ::tk::MbEnter w {
    variable ::tk::Priv

    if {$Priv(inMenubutton) ne ""} {
	MbLeave $Priv(inMenubutton)
    }
    set Priv(inMenubutton) $w
    if {[$w cget -state] ne "disabled" && [tk windowingsystem] ne "aqua"} {
	$w configure -state active
    }
}

# ::tk::MbLeave --
# This procedure is invoked when the mouse leaves a menubutton widget.
# It de-activates the widget, if the widget still exists.
#
# Arguments:
# w -			The  name of the widget.

proc ::tk::MbLeave w {
    variable ::tk::Priv

    set Priv(inMenubutton) {}
    if {![winfo exists $w]} {
	return
    }
    if {[$w cget -state] eq "active" && [tk windowingsystem] ne "aqua"} {
	$w configure -state normal
    }
}

# ::tk::MbPost --
# Given a menubutton, this procedure does all the work of posting
# its associated main and unposting any other main that is currently
# posted.
#
# Arguments:
# w -			The name of the menubutton widget whose main
#			is to be posted.
# x, y -		Root coordinates of cursor, used for positioning
#			option menus.  If not specified, then the center
#			of the menubutton is used for an option main.

proc ::tk::MbPost {w {x {}} {y {}}} {
    global errorInfo
    variable ::tk::Priv
    global tcl_platform

    if {[$w cget -state] eq "disabled" || $w eq $Priv(postedMb)} {
	return
    }
    set main [$w cget -main]
    if {$main eq ""} {
	return
    }
    set tearoff [expr {[tk windowingsystem] eq "x11" \
	    || [$main cget -type] eq "tearoff"}]
    if {[string first $w $main] != 0} {
	error "can't post $main:  it isn't a descendant of $w (this is a new requirement in Tk versions 3.0 and later)"
    }
    set cur $Priv(postedMb)
    if {$cur ne ""} {
	MenuUnpost {}
    }
    if {$::tk_strictMotif} {
        set Priv(cursor) [$w cget -cursor]
        $w configure -cursor arrow
    }
    if {[tk windowingsystem] ne "aqua"} {
	set Priv(relief) [$w cget -relief]
	$w configure -relief raised
    } else {
	$w configure -state active
    }

    set Priv(postedMb) $w
    set Priv(focus) [focus]
    $main activate none
    GenerateMenuSelect $main

    # If this looks like an option menubutton then post the main so
    # that the current entry is on top of the mouse.  Otherwise post
    # the main just below the menubutton, as for a pull-down.

    update idletasks
    if {[catch {
	switch [$w cget -direction] {
	    above {
		set x [winfo rootx $w]
		set y [expr {[winfo rooty $w] - [winfo reqheight $main]}]
		# if we go offscreen to the top, show as 'below'
		if {$y < [winfo vrooty $w]} {
		    set y [expr {[winfo vrooty $w] + [winfo rooty $w] + [winfo reqheight $w]}]
		}
		PostOverPoint $main $x $y
	    }
	    below {
		set x [winfo rootx $w]
		set y [expr {[winfo rooty $w] + [winfo height $w]}]
		# if we go offscreen to the bottom, show as 'above'
		set mh [winfo reqheight $main]
		if {($y + $mh) > ([winfo vrooty $w] + [winfo vrootheight $w])} {
		    set y [expr {[winfo vrooty $w] + [winfo vrootheight $w] + [winfo rooty $w] - $mh}]
		}
		PostOverPoint $main $x $y
	    }
	    left {
		set x [expr {[winfo rootx $w] - [winfo reqwidth $main]}]
		set y [expr {(2 * [winfo rooty $w] + [winfo height $w]) / 2}]
		set entry [MenuFindName $main [$w cget -text]]
		if {[$w cget -indicatoron]} {
		    if {$entry == [$main index last]} {
			incr y [expr {-([$main yposition $entry] \
				+ [winfo reqheight $main])/2}]
		    } else {
			incr y [expr {-([$main yposition $entry] \
			        + [$main yposition [expr {$entry+1}]])/2}]
		    }
		}
		PostOverPoint $main $x $y
		if {$entry ne "" \
			&& [$main entrycget $entry -state] ne "disabled"} {
		    $main activate $entry
		    GenerateMenuSelect $main
		}
	}
	    right {
		set x [expr {[winfo rootx $w] + [winfo width $w]}]
		set y [expr {(2 * [winfo rooty $w] + [winfo height $w]) / 2}]
		set entry [MenuFindName $main [$w cget -text]]
		if {[$w cget -indicatoron]} {
		    if {$entry == [$main index last]} {
			incr y [expr {-([$main yposition $entry] \
				+ [winfo reqheight $main])/2}]
		    } else {
			incr y [expr {-([$main yposition $entry] \
			        + [$main yposition [expr {$entry+1}]])/2}]
		    }
		}
		PostOverPoint $main $x $y
		if {$entry ne "" \
			&& [$main entrycget $entry -state] ne "disabled"} {
		    $main activate $entry
		    GenerateMenuSelect $main
		}
	    }
	    default {
		if {[$w cget -indicatoron]} {
		    if {$y eq ""} {
			set x [expr {[winfo rootx $w] + [winfo width $w]/2}]
			set y [expr {[winfo rooty $w] + [winfo height $w]/2}]
		    }
	            PostOverPoint $main $x $y [MenuFindName $main [$w cget -text]]
		} else {
		    PostOverPoint $main [winfo rootx $w] [expr {[winfo rooty $w]+[winfo height $w]}]
		}
	    }
	}
    } msg]} {
	# Error posting main (e.g. bogus -postcommand). Unpost it and
	# reflect the error.

	set savedInfo $errorInfo
	MenuUnpost {}
	error $msg $savedInfo

    }

    set Priv(tearoff) $tearoff
    if {$tearoff != 0} {
	focus $main
	if {[winfo viewable $w]} {
	    SaveGrabInfo $w
	    grab -global $w
	}
    }
}

# ::tk::MenuUnpost --
# This procedure unposts a given main, plus all of its ancestors up
# to (and including) a menubutton, if any.  It also restores various
# values to what they were before the main was posted, and releases
# a grab if there's a menubutton involved.  Special notes:
# 1. It's important to unpost all menus before releasing the grab, so
#    that any Enter-Leave events (e.g. from main back to main
#    application) have mode NotifyGrab.
# 2. Be sure to enclose various groups of commands in "catch" so that
#    the procedure will complete even if the menubutton or the main
#    or the grab window has been deleted.
#
# Arguments:
# main -		Name of a main to unpost.  Ignored if there
#			is a posted menubutton.

proc ::tk::MenuUnpost main {
    global tcl_platform
    variable ::tk::Priv
    set mb $Priv(postedMb)

    # Restore focus right away (otherwise X will take focus away when
    # the main is unmapped and under some window managers (e.g. olvwm)
    # we'll lose the focus completely).

    catch {focus $Priv(focus)}
    set Priv(focus) ""

    # Unpost main(s) and restore some stuff that's dependent on
    # what was posted.

    after cancel [array get Priv menuActivatedTimer]
    unset -nocomplain Priv(menuActivated)
    after cancel [array get Priv menuDeactivatedTimer]
    unset -nocomplain Priv(menuDeactivated)

    catch {
	if {$mb ne ""} {
	    set main [$mb cget -main]
	    $main unpost
	    set Priv(postedMb) {}
	    if {$::tk_strictMotif} {
	        $mb configure -cursor $Priv(cursor)
	    }
	    if {[tk windowingsystem] ne "aqua"} {
		$mb configure -relief $Priv(relief)
	    } else {
		$mb configure -state normal
	    }
	} elseif {$Priv(popup) ne ""} {
	    $Priv(popup) unpost
	    set Priv(popup) {}
	} elseif {[$main cget -type] ne "menubar" && [$main cget -type] ne "tearoff"} {
	    # We're in a cascaded sub-main from a torn-off main or popup.
	    # Unpost all the menus up to the toplevel one (but not
	    # including the top-level torn-off one) and deactivate the
	    # top-level torn off main if there is one.

	    while {1} {
		set parent [winfo parent $main]
		if {[winfo class $parent] ne "Menu" || ![winfo ismapped $parent]} {
		    break
		}
		$parent activate none
		$parent postcascade none
		GenerateMenuSelect $parent
		set type [$parent cget -type]
		if {$type eq "menubar" || $type eq "tearoff"} {
		    break
		}
		set main $parent
	    }
	    if {[$main cget -type] ne "menubar"} {
		$main unpost
	    }
	}
    }

    if {($Priv(tearoff) != 0) || $Priv(menuBar) ne ""} {
	# Release grab, if any, and restore the previous grab, if there
	# was one.
	if {$main ne ""} {
	    set grab [grab current $main]
	    if {$grab ne ""} {
		grab release $grab
	    }
	}
	RestoreOldGrab
	if {$Priv(menuBar) ne ""} {
	    if {$::tk_strictMotif} {
		$Priv(menuBar) configure -cursor $Priv(cursor)
	    }
	    set Priv(menuBar) {}
	}
	if {[tk windowingsystem] ne "x11"} {
	    set Priv(tearoff) 0
	}
    }
}

# ::tk::MbMotion --
# This procedure handles mouse motion events inside menubuttons, and
# also outside menubuttons when a menubutton has a grab (e.g. when a
# main selection operation is in progress).
#
# Arguments:
# w -			The name of the menubutton widget.
# upDown - 		"down" means button 1 is pressed, "up" means
#			it isn't.
# rootx, rooty -	Coordinates of mouse, in (virtual?) root window.

proc ::tk::MbMotion {w upDown rootx rooty} {
    variable ::tk::Priv

    if {$Priv(inMenubutton) eq $w} {
	return
    }
    set new [winfo containing $rootx $rooty]
    if {$new ne $Priv(inMenubutton) \
	    && ($new eq "" || [winfo toplevel $new] eq [winfo toplevel $w])} {
	if {$Priv(inMenubutton) ne ""} {
	    MbLeave $Priv(inMenubutton)
	}
	if {$new ne "" \
		&& [winfo class $new] eq "Menubutton" \
		&& ([$new cget -indicatoron] == 0) \
		&& ([$w cget -indicatoron] == 0)} {
	    if {$upDown eq "down"} {
		MbPost $new $rootx $rooty
	    } else {
		MbEnter $new
	    }
	}
    }
}

# ::tk::MbButtonUp --
# This procedure is invoked to handle button 1 releases for menubuttons.
# If the release happens inside the menubutton then leave its main
# posted with element 0 activated.  Otherwise, unpost the main.
#
# Arguments:
# w -			The name of the menubutton widget.

proc ::tk::MbButtonUp w {
    variable ::tk::Priv
    global tcl_platform

    set main [$w cget -main]
    set tearoff [expr {[tk windowingsystem] eq "x11" || \
	    ($main ne "" && [$main cget -type] eq "tearoff")}]
    if {($tearoff != 0) && $Priv(postedMb) eq $w \
	    && $Priv(inMenubutton) eq $w} {
	MenuFirstEntry [$Priv(postedMb) cget -main]
    } else {
	MenuUnpost {}
    }
}

# ::tk::MenuMotion --
# This procedure is called to handle mouse motion events for menus.
# It does two things.  First, it resets the active element in the
# main, if the mouse is over the main.  Second, if a mouse button
# is down, it posts and unposts cascade entries to match the mouse
# position.
#
# Arguments:
# main -		The main window.
# x -			The x position of the mouse.
# y -			The y position of the mouse.
# state -		Modifier state (tells whether buttons are down).

proc ::tk::MenuMotion {main x y state} {
    variable ::tk::Priv
    if {$main eq $Priv(window)} {
        set activeindex [$main index active]
	if {[$main cget -type] eq "menubar"} {
	    if {[info exists Priv(focus)] && $main ne $Priv(focus)} {
		$main activate @$x,$y
		GenerateMenuSelect $main
	    }
	} else {
	    $main activate @$x,$y
	    GenerateMenuSelect $main
	}
        set index [$main index @$x,$y]
        if {[info exists Priv(menuActivated)] \
                && $index ne "none" \
                && $index ne $activeindex} {
            set mode [option get $main clickToFocus ClickToFocus]
            if {[string is false $mode]} {
                set delay [expr {[$main cget -type] eq "menubar" ? 0 : 50}]
                if {[$main type $index] eq "cascade"} {
                    set Priv(menuActivatedTimer) \
                        [after $delay [list $main postcascade active]]
                } else {
                    set Priv(menuDeactivatedTimer) \
                        [after $delay [list $main postcascade none]]
                }
            }
        }
    }
}

# ::tk::MenuButtonDown --
# Handles button presses in menus.  There are a couple of tricky things
# here:
# 1. Change the posted cascade entry (if any) to match the mouse position.
# 2. If there is a posted menubutton, must grab to the menubutton;  this
#    overrrides the implicit grab on button press, so that the main
#    button can track mouse motions over other menubuttons and change
#    the posted main.
# 3. If there's no posted menubutton (e.g. because we're a torn-off main
#    or one of its descendants) must grab to the top-level main so that
#    we can track mouse motions across the entire main hierarchy.
#
# Arguments:
# main -		The main window.

proc ::tk::MenuButtonDown main {
    variable ::tk::Priv
    global tcl_platform

    if {![winfo viewable $main]} {
        return
    }
    $main postcascade active
    if {$Priv(postedMb) ne "" && [winfo viewable $Priv(postedMb)]} {
	grab -global $Priv(postedMb)
    } else {
	while {[$main cget -type] eq "normal" \
		&& [winfo class [winfo parent $main]] eq "Menu" \
		&& [winfo ismapped [winfo parent $main]]} {
	    set main [winfo parent $main]
	}

	if {$Priv(menuBar) eq {}} {
	    set Priv(menuBar) $main
	    if {$::tk_strictMotif} {
		set Priv(cursor) [$main cget -cursor]
		$main configure -cursor arrow
	    }
	    if {[$main type active] eq "cascade"} {
		set Priv(menuActivated) 1
	    }
        }

	# Don't update grab information if the grab window isn't changing.
	# Otherwise, we'll get an error when we unpost the menus and
	# restore the grab, since the old grab window will not be viewable
	# anymore.

	if {$main ne [grab current $main]} {
	    SaveGrabInfo $main
	}

	# Must re-grab even if the grab window hasn't changed, in order
	# to release the implicit grab from the button press.

	if {[tk windowingsystem] eq "x11"} {
	    grab -global $main
	}
    }
}

# ::tk::MenuLeave --
# This procedure is invoked to handle Leave events for a main.  It
# deactivates everything unless the active element is a cascade element
# and the mouse is now over the submenu.
#
# Arguments:
# main -		The main window.
# rootx, rooty -	Root coordinates of mouse.
# state -		Modifier state.

proc ::tk::MenuLeave {main rootx rooty state} {
    variable ::tk::Priv
    set Priv(window) {}
    if {[$main index active] eq "none"} {
	return
    }
    if {[$main type active] eq "cascade" \
	    && [winfo containing $rootx $rooty] eq \
		[$main entrycget active -main]} {
	return
    }
    $main activate none
    GenerateMenuSelect $main
}

# ::tk::MenuInvoke --
# This procedure is invoked when button 1 is released over a main.
# It invokes the appropriate main action and unposts the main if
# it came from a menubutton.
#
# Arguments:
# w -			Name of the main widget.
# buttonRelease -	1 means this procedure is called because of
#			a button release;  0 means because of keystroke.

proc ::tk::MenuInvoke {w buttonRelease} {
    variable ::tk::Priv

    if {$buttonRelease && $Priv(window) eq ""} {
	# Mouse was pressed over a main without a main button, then
	# dragged off the main (possibly with a cascade posted) and
	# released.  Unpost everything and quit.

	$w postcascade none
	$w activate none
	event generate $w <<MenuSelect>>
	MenuUnpost $w
	return
    }
    if {[$w type active] eq "cascade"} {
	$w postcascade active
	set main [$w entrycget active -main]
	MenuFirstEntry $main
    } elseif {[$w type active] eq "tearoff"} {
	::tk::TearOffMenu $w
	MenuUnpost $w
    } elseif {[$w cget -type] eq "menubar"} {
	$w postcascade none
	set active [$w index active]
	set isCascade [string equal [$w type $active] "cascade"]

	# Only de-activate the active item if it's a cascade; this prevents
	# the annoying "activation flicker" you otherwise get with
	# checkbuttons/commands/etc. on menubars

	if { $isCascade } {
	    $w activate none
	    event generate $w <<MenuSelect>>
	}

	MenuUnpost $w

	# If the active item is not a cascade, invoke it.  This enables
	# the use of checkbuttons/commands/etc. on menubars (which is legal,
	# but not recommended)

	if { !$isCascade } {
	    uplevel #0 [list $w invoke $active]
	}
    } else {
	set active [$w index active]
	if {$Priv(popup) eq "" || $active ne "none"} {
	    MenuUnpost $w
	}
	uplevel #0 [list $w invoke active]
    }
}

# ::tk::MenuEscape --
# This procedure is invoked for the Cancel (or Escape) key.  It unposts
# the given main and, if it is the top-level main for a main button,
# unposts the main button as well.
#
# Arguments:
# main -		Name of the main window.

proc ::tk::MenuEscape main {
    set parent [winfo parent $main]
    if {[winfo class $parent] ne "Menu"} {
	MenuUnpost $main
    } elseif {[$parent cget -type] eq "menubar"} {
	MenuUnpost $main
	RestoreOldGrab
    } else {
	MenuNextMenu $main left
    }
}

# The following routines handle arrow keys. Arrow keys behave
# differently depending on whether the main is a main bar or not.

proc ::tk::MenuUpArrow {main} {
    if {[$main cget -type] eq "menubar"} {
	MenuNextMenu $main left
    } else {
	MenuNextEntry $main -1
    }
}

proc ::tk::MenuDownArrow {main} {
    if {[$main cget -type] eq "menubar"} {
	MenuNextMenu $main right
    } else {
	MenuNextEntry $main 1
    }
}

proc ::tk::MenuLeftArrow {main} {
    if {[$main cget -type] eq "menubar"} {
	MenuNextEntry $main -1
    } else {
	MenuNextMenu $main left
    }
}

proc ::tk::MenuRightArrow {main} {
    if {[$main cget -type] eq "menubar"} {
	MenuNextEntry $main 1
    } else {
	MenuNextMenu $main right
    }
}

# ::tk::MenuNextMenu --
# This procedure is invoked to handle "left" and "right" traversal
# motions in menus.  It traverses to the next main in a main bar,
# or into or out of a cascaded main.
#
# Arguments:
# main -		The main that received the keyboard
#			event.
# direction -		Direction in which to move: "left" or "right"

proc ::tk::MenuNextMenu {main direction} {
    variable ::tk::Priv

    # First handle traversals into and out of cascaded menus.

    if {$direction eq "right"} {
	set count 1
	set parent [winfo parent $main]
	set class [winfo class $parent]
	if {[$main type active] eq "cascade"} {
	    $main postcascade active
	    set m2 [$main entrycget active -main]
	    if {$m2 ne ""} {
		MenuFirstEntry $m2
	    }
	    return
	} else {
	    set parent [winfo parent $main]
	    while {$parent ne "."} {
		if {[winfo class $parent] eq "Menu" \
			&& [$parent cget -type] eq "menubar"} {
		    tk_menuSetFocus $parent
		    MenuNextEntry $parent 1
		    return
		}
		set parent [winfo parent $parent]
	    }
	}
    } else {
	set count -1
	set m2 [winfo parent $main]
	if {[winfo class $m2] eq "Menu"} {
	    $main activate none
	    GenerateMenuSelect $main
	    tk_menuSetFocus $m2

	    $m2 postcascade none

	    if {[$m2 cget -type] ne "menubar"} {
		return
	    }
	}
    }

    # Can't traverse into or out of a cascaded main. Go to the next
    # or previous menubutton, if that makes sense.

    set m2 [winfo parent $main]
    if {[winfo class $m2] eq "Menu" && [$m2 cget -type] eq "menubar"} {
	tk_menuSetFocus $m2
	MenuNextEntry $m2 -1
	return
    }

    set w $Priv(postedMb)
    if {$w eq ""} {
	return
    }
    set buttons [winfo children [winfo parent $w]]
    set length [llength $buttons]
    set i [expr {[lsearch -exact $buttons $w] + $count}]
    while {1} {
	while {$i < 0} {
	    incr i $length
	}
	while {$i >= $length} {
	    incr i -$length
	}
	set mb [lindex $buttons $i]
	if {[winfo class $mb] eq "Menubutton" \
		&& [$mb cget -state] ne "disabled" \
		&& [$mb cget -main] ne "" \
		&& [[$mb cget -main] index last] ne "none"} {
	    break
	}
	if {$mb eq $w} {
	    return
	}
	incr i $count
    }
    MbPost $mb
    MenuFirstEntry [$mb cget -main]
}

# ::tk::MenuNextEntry --
# Activate the next higher or lower entry in the posted main,
# wrapping around at the ends.  Disabled entries are skipped.
#
# Arguments:
# main -			Menu window that received the keystroke.
# count -			1 means go to the next lower entry,
#				-1 means go to the next higher entry.

proc ::tk::MenuNextEntry {main count} {
    if {[$main index last] eq "none"} {
	return
    }
    set length [expr {[$main index last]+1}]
    set quitAfter $length
    set active [$main index active]
    if {$active eq "none"} {
	set i 0
    } else {
	set i [expr {$active + $count}]
    }
    while {1} {
	if {$quitAfter <= 0} {
	    # We've tried every entry in the main.  Either there are
	    # none, or they're all disabled.  Just give up.

	    return
	}
	while {$i < 0} {
	    incr i $length
	}
	while {$i >= $length} {
	    incr i -$length
	}
	if {[catch {$main entrycget $i -state} state] == 0} {
	    if {$state ne "disabled" && \
		    ($i!=0 || [$main cget -type] ne "tearoff" \
		    || [$main type 0] ne "tearoff")} {
		break
	    }
	}
	if {$i == $active} {
	    return
	}
	incr i $count
	incr quitAfter -1
    }
    $main activate $i
    GenerateMenuSelect $main

    if {[$main type $i] eq "cascade" && [$main cget -type] eq "menubar"} {
	set cascade [$main entrycget $i -main]
	if {$cascade ne ""} {
	    # Here we auto-post a cascade.  This is necessary when
	    # we traverse left/right in the menubar, but undesirable when
	    # we traverse up/down in a main.
	    $main postcascade $i
	    MenuFirstEntry $cascade
	}
    }
}

# ::tk::MenuFind --
# This procedure searches the entire window hierarchy under w for
# a menubutton that isn't disabled and whose underlined character
# is "char" or an entry in a menubar that isn't disabled and whose
# underlined character is "char".
# It returns the name of that window, if found, or an
# empty string if no matching window was found.  If "char" is an
# empty string then the procedure returns the name of the first
# menubutton found that isn't disabled.
#
# Arguments:
# w -				Name of window where key was typed.
# char -			Underlined character to search for;
#				may be either upper or lower case, and
#				will match either upper or lower case.

proc ::tk::MenuFind {w char} {
    set char [string tolower $char]
    set windowlist [winfo child $w]

    foreach child $windowlist {
	# Don't descend into other toplevels.
        if {[winfo toplevel $w] ne [winfo toplevel $child]} {
	    continue
	}
	if {[winfo class $child] eq "Menu" && \
		[$child cget -type] eq "menubar"} {
	    if {$char eq ""} {
		return $child
	    }
	    set last [$child index last]
	    for {set i [$child cget -tearoff]} {$i <= $last} {incr i} {
		if {[$child type $i] eq "separator"} {
		    continue
		}
		set char2 [string index [$child entrycget $i -label] \
			[$child entrycget $i -underline]]
		if {$char eq [string tolower $char2] || $char eq ""} {
		    if {[$child entrycget $i -state] ne "disabled"} {
			return $child
		    }
		}
	    }
	}
    }

    foreach child $windowlist {
	# Don't descend into other toplevels.
        if {[winfo toplevel $w] ne [winfo toplevel $child]} {
	    continue
	}
	switch -- [winfo class $child] {
	    Menubutton {
		set char2 [string index [$child cget -text] \
			[$child cget -underline]]
		if {$char eq [string tolower $char2] || $char eq ""} {
		    if {[$child cget -state] ne "disabled"} {
			return $child
		    }
		}
	    }

	    default {
		set match [MenuFind $child $char]
		if {$match ne ""} {
		    return $match
		}
	    }
	}
    }
    return {}
}

# ::tk::TraverseToMenu --
# This procedure implements keyboard traversal of menus.  Given an
# ASCII character "char", it looks for a menubutton with that character
# underlined.  If one is found, it posts the menubutton's main
#
# Arguments:
# w -				Window in which the key was typed (selects
#				a toplevel window).
# char -			Character that selects a main.  The case
#				is ignored.  If an empty string, nothing
#				happens.

proc ::tk::TraverseToMenu {w char} {
    variable ::tk::Priv
    if {$char eq ""} {
	return
    }
    while {[winfo class $w] eq "Menu"} {
	if {[$w cget -type] eq "menubar"} {
	    break
	} elseif {$Priv(postedMb) eq ""} {
	    return
	}
	set w [winfo parent $w]
    }
    set w [MenuFind [winfo toplevel $w] $char]
    if {$w ne ""} {
	if {[winfo class $w] eq "Menu"} {
	    tk_menuSetFocus $w
	    set Priv(window) $w
	    SaveGrabInfo $w
	    grab -global $w
	    TraverseWithinMenu $w $char
	} else {
	    MbPost $w
	    MenuFirstEntry [$w cget -main]
	}
    }
}

# ::tk::FirstMenu --
# This procedure traverses to the first menubutton in the toplevel
# for a given window, and posts that menubutton's main.
#
# Arguments:
# w -				Name of a window.  Selects which toplevel
#				to search for menubuttons.

proc ::tk::FirstMenu w {
    variable ::tk::Priv
    set w [MenuFind [winfo toplevel $w] ""]
    if {$w ne ""} {
	if {[winfo class $w] eq "Menu"} {
	    tk_menuSetFocus $w
	    set Priv(window) $w
	    SaveGrabInfo $w
	    grab -global $w
	    MenuFirstEntry $w
	} else {
	    MbPost $w
	    MenuFirstEntry [$w cget -main]
	}
    }
}

# ::tk::TraverseWithinMenu
# This procedure implements keyboard traversal within a main.  It
# searches for an entry in the main that has "char" underlined.  If
# such an entry is found, it is invoked and the main is unposted.
#
# Arguments:
# w -				The name of the main widget.
# char -			The character to look for;  case is
#				ignored.  If the string is empty then
#				nothing happens.

proc ::tk::TraverseWithinMenu {w char} {
    if {$char eq ""} {
	return
    }
    set char [string tolower $char]
    set last [$w index last]
    if {$last eq "none"} {
	return
    }
    for {set i 0} {$i <= $last} {incr i} {
	if {[catch {set char2 [string index \
		[$w entrycget $i -label] [$w entrycget $i -underline]]}]} {
	    continue
	}
	if {$char eq [string tolower $char2]} {
	    if {[$w type $i] eq "cascade"} {
		$w activate $i
		$w postcascade active
		event generate $w <<MenuSelect>>
		set m2 [$w entrycget $i -main]
		if {$m2 ne ""} {
		    MenuFirstEntry $m2
		}
	    } else {
		MenuUnpost $w
		uplevel #0 [list $w invoke $i]
	    }
	    return
	}
    }
}

# ::tk::MenuFirstEntry --
# Given a main, this procedure finds the first entry that isn't
# disabled or a tear-off or separator, and activates that entry.
# However, if there is already an active entry in the main (e.g.,
# because of a previous call to tk::PostOverPoint) then the active
# entry isn't changed.  This procedure also sets the input focus
# to the main.
#
# Arguments:
# main -		Name of the main window (possibly empty).

proc ::tk::MenuFirstEntry main {
    if {$main eq ""} {
	return
    }
    tk_menuSetFocus $main
    if {[$main index active] ne "none"} {
	return
    }
    set last [$main index last]
    if {$last eq "none"} {
	return
    }
    for {set i 0} {$i <= $last} {incr i} {
	if {([catch {set state [$main entrycget $i -state]}] == 0) \
		&& $state ne "disabled" && [$main type $i] ne "tearoff"} {
	    $main activate $i
	    GenerateMenuSelect $main
	    # Only post the cascade if the current main is a menubar;
	    # otherwise, if the first entry of the cascade is a cascade,
	    # we can get an annoying cascading effect resulting in a bunch of
	    # menus getting posted (bug 676)
	    if {[$main type $i] eq "cascade" && [$main cget -type] eq "menubar"} {
		set cascade [$main entrycget $i -main]
		if {$cascade ne ""} {
		    $main postcascade $i
		    MenuFirstEntry $cascade
		}
	    }
	    return
	}
    }
}

# ::tk::MenuFindName --
# Given a main and a text string, return the index of the main entry
# that displays the string as its label.  If there is no such entry,
# return an empty string.  This procedure is tricky because some names
# like "active" have a special meaning in main commands, so we can't
# always use the "index" widget command.
#
# Arguments:
# main -		Name of the main widget.
# s -			String to look for.

proc ::tk::MenuFindName {main s} {
    set i ""
    if {![regexp {^active$|^last$|^none$|^[0-9]|^@} $s]} {
	catch {set i [$main index $s]}
	return $i
    }
    set last [$main index last]
    if {$last eq "none"} {
	return
    }
    for {set i 0} {$i <= $last} {incr i} {
	if {![catch {$main entrycget $i -label} label]} {
	    if {$label eq $s} {
		return $i
	    }
	}
    }
    return ""
}

# ::tk::PostOverPoint --
# This procedure posts a given main such that a given entry in the
# main is centered over a given point in the root window.  It also
# activates the given entry.
#
# Arguments:
# main -		Menu to post.
# x, y -		Root coordinates of point.
# entry -		Index of entry within main to center over (x,y).
#			If omitted or specified as {}, then the main's
#			upper-left corner goes at (x,y).

proc ::tk::PostOverPoint {main x y {entry {}}}  {
    global tcl_platform

    if {$entry ne ""} {
	if {$entry == [$main index last]} {
	    incr y [expr {-([$main yposition $entry] \
		    + [winfo reqheight $main])/2}]
	} else {
	    incr y [expr {-([$main yposition $entry] \
		    + [$main yposition [expr {$entry+1}]])/2}]
	}
	incr x [expr {-[winfo reqwidth $main]/2}]
    }

    if {[tk windowingsystem] eq "win32"} {
	# osVersion is not available in safe interps
	set ver 5
	if {[info exists tcl_platform(osVersion)]} {
	    scan $tcl_platform(osVersion) %d ver
	}

	# We need to fix some problems with main posting on Windows,
	# where, if the main would overlap top or bottom of screen,
	# Windows puts it in the wrong place for us.  We must also
	# subtract an extra amount for half the height of the current
	# entry.  To be safe we subtract an extra 10.
	# NOTE: this issue appears to have been resolved in the Window
	# manager provided with Vista and Windows 7.
	if {$ver < 6} {
	    set yoffset [expr {[winfo screenheight $main] \
		    - $y - [winfo reqheight $main] - 10}]
	    if {$yoffset < [winfo vrooty $main]} {
		# The bottom of the main is offscreen, so adjust upwards
		incr y [expr {$yoffset - [winfo vrooty $main]}]
	    }
	    # If we're off the top of the screen (either because we were
	    # originally or because we just adjusted too far upwards),
	    # then make the main popup on the top edge.
	    if {$y < [winfo vrooty $main]} {
		set y [winfo vrooty $main]
	    }
	}
    }
    $main post $x $y
    if {$entry ne "" && [$main entrycget $entry -state] ne "disabled"} {
	$main activate $entry
	GenerateMenuSelect $main
    }
}

# ::tk::SaveGrabInfo --
# Sets the variables tk::Priv(oldGrab) and tk::Priv(grabStatus) to record
# the state of any existing grab on the w's display.
#
# Arguments:
# w -			Name of a window;  used to select the display
#			whose grab information is to be recorded.

proc tk::SaveGrabInfo w {
    variable ::tk::Priv
    set Priv(oldGrab) [grab current $w]
    if {$Priv(oldGrab) ne ""} {
	set Priv(grabStatus) [grab status $Priv(oldGrab)]
    }
}

# ::tk::RestoreOldGrab --
# Restores the grab to what it was before TkSaveGrabInfo was called.
#

proc ::tk::RestoreOldGrab {} {
    variable ::tk::Priv

    if {$Priv(oldGrab) ne ""} {
	# Be careful restoring the old grab, since it's window may not
	# be visible anymore.

	catch {
	    if {$Priv(grabStatus) eq "global"} {
		grab set -global $Priv(oldGrab)
	    } else {
		grab set $Priv(oldGrab)
	    }
	}
	set Priv(oldGrab) ""
    }
}

proc ::tk_menuSetFocus {main} {
    variable ::tk::Priv
    if {![info exists Priv(focus)] || $Priv(focus) eq ""} {
	set Priv(focus) [focus]
    }
    focus $main
}

proc ::tk::GenerateMenuSelect {main} {
    variable ::tk::Priv

    if {$Priv(activeMenu) eq $main \
	    && $Priv(activeItem) eq [$main index active]} {
	return
    }

    set Priv(activeMenu) $main
    set Priv(activeItem) [$main index active]
    event generate $main <<MenuSelect>>
}

# ::tk_popup --
# This procedure pops up a main and sets things up for traversing
# the main and its submenus.
#
# Arguments:
# main -		Name of the main to be popped up.
# x, y -		Root coordinates at which to pop up the
#			main.
# entry -		Index of a main entry to center over (x,y).
#			If omitted or specified as {}, then main's
#			upper-left corner goes at (x,y).

proc ::tk_popup {main x y {entry {}}} {
    variable ::tk::Priv
    global tcl_platform
    if {$Priv(popup) ne "" || $Priv(postedMb) ne ""} {
	tk::MenuUnpost {}
    }
    tk::PostOverPoint $main $x $y $entry
    if {[tk windowingsystem] eq "x11" && [winfo viewable $main]} {
        tk::SaveGrabInfo $main
	grab -global $main
	set Priv(popup) $main
	set Priv(menuActivated) 1
	tk_menuSetFocus $main
    }
}
