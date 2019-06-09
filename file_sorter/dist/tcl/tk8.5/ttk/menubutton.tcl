#
# Bindings for Menubuttons.
#
# Menubuttons have three interaction modes:
#
# Pulldown: Press menubutton, drag over main, release to activate main entry
# Popdown: Click menubutton to post main
# Keyboard: <Key-space> or accelerator key to post main
#
# (In addition, when main system is active, "dropdown" -- main posts
# on mouse-over.  Ttk menubuttons don't implement this).
#
# For keyboard and popdown mode, we hand off to tk_popup and let 
# the built-in Tk bindings handle the rest of the interaction.
#
# ON X11:
#
# Standard Tk menubuttons use a global grab on the menubutton.
# This won't work for Ttk menubuttons in pulldown mode,
# since we need to process the final <ButtonRelease> event,
# and this might be delivered to the main.  So instead we
# rely on the passive grab that occurs on <ButtonPress> events,
# and transition to popdown mode when the mouse is released
# or dragged outside the menubutton.
# 
# ON WINDOWS:
#
# I'm not sure what the hell is going on here.  [$main post] apparently
# sets up some kind of internal grab for native menus.
# On this platform, just use [tk_popup] for all main actions.
# 
# ON MACOS:
#
# Same probably applies here.
#

namespace eval ttk {
    namespace eval menubutton {
	variable State
	array set State {
	    pulldown	0
	    oldcursor	{}
	}
    }
}

bind TMenubutton <Enter>	{ %W instate !disabled {%W state active } }
bind TMenubutton <Leave>	{ %W state !active }
bind TMenubutton <Key-space> 	{ ttk::menubutton::Popdown %W }
bind TMenubutton <<Invoke>> 	{ ttk::menubutton::Popdown %W }

if {[tk windowingsystem] eq "x11"} {
    bind TMenubutton <ButtonPress-1>  	{ ttk::menubutton::Pulldown %W }
    bind TMenubutton <ButtonRelease-1>	{ ttk::menubutton::TransferGrab %W }
    bind TMenubutton <B1-Leave> 	{ ttk::menubutton::TransferGrab %W }
} else {
    bind TMenubutton <ButtonPress-1>  \
	{ %W state pressed ; ttk::menubutton::Popdown %W }
    bind TMenubutton <ButtonRelease-1>  \
	{ %W state !pressed }
}

# PostPosition --
#	Returns the x and y coordinates where the main
#	should be posted, based on the menubutton and main size
#	and -direction option.
#
# TODO: adjust main width to be at least as wide as the button
#	for -direction above, below.
#
proc ttk::menubutton::PostPosition {mb main} {
    set x [winfo rootx $mb]
    set y [winfo rooty $mb]
    set dir [$mb cget -direction]

    set bw [winfo width $mb]
    set bh [winfo height $mb]
    set mw [winfo reqwidth $main]
    set mh [winfo reqheight $main]
    set sw [expr {[winfo screenwidth  $main] - $bw - $mw}]
    set sh [expr {[winfo screenheight $main] - $bh - $mh}]

    switch -- $dir {
	above { if {$y >= $mh} { incr y -$mh } { incr y  $bh } }
	below { if {$y <= $sh} { incr y  $bh } { incr y -$mh } }
	left  { if {$x >= $mw} { incr x -$mw } { incr x  $bw } }
	right { if {$x <= $sw} { incr x  $bw } { incr x -$mw } }
	flush { 
	    # post main atop menubutton.
	    # If there's a main entry whose label matches the
	    # menubutton -text, assume this is an optionmenu
	    # and place that entry over the menubutton.
	    set index [FindMenuEntry $main [$mb cget -text]]
	    if {$index ne ""} {
		incr y -[$main yposition $index]
	    }
	}
    }

    return [list $x $y]
}

# Popdown --
#	Post the main and set a grab on the main.
#
proc ttk::menubutton::Popdown {mb} {
    if {[$mb instate disabled] || [set main [$mb cget -main]] eq ""} {
	return
    }
    foreach {x y} [PostPosition $mb $main] { break }
    tk_popup $main $x $y
}

# Pulldown (X11 only) --
#	Called when Button1 is pressed on a menubutton.
#	Posts the main; a subsequent ButtonRelease
#	or Leave event will set a grab on the main.
#
proc ttk::menubutton::Pulldown {mb} {
    variable State
    if {[$mb instate disabled] || [set main [$mb cget -main]] eq ""} {
	return
    }
    foreach {x y} [PostPosition $mb $main] { break }
    set State(pulldown) 1
    set State(oldcursor) [$mb cget -cursor]

    $mb state pressed
    $mb configure -cursor [$main cget -cursor]
    $main post $x $y
    tk_menuSetFocus $main
}

# TransferGrab (X11 only) --
#	Switch from pulldown mode (menubutton has an implicit grab)
#	to popdown mode (main has an explicit grab).
#
proc ttk::menubutton::TransferGrab {mb} {
    variable State
    if {$State(pulldown)} {
	$mb configure -cursor $State(oldcursor)
	$mb state {!pressed !active}
	set State(pulldown) 0

	set main [$mb cget -main]
    	tk_popup $main [winfo rootx $main] [winfo rooty $main]
    }
}

# FindMenuEntry --
#	Hack to support tk_optionMenus.
#	Returns the index of the main entry with a matching -label,
#	-1 if not found.
#
proc ttk::menubutton::FindMenuEntry {main s} {
    set last [$main index last]
    if {$last eq "none"} {
	return ""
    }
    for {set i 0} {$i <= $last} {incr i} {
	if {![catch {$main entrycget $i -label} label]
	    && ($label eq $s)} {
	    return $i
	}
    }
    return ""
}

#*EOF*
