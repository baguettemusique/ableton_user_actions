"""
ClyphX_Pro allows you to add your own actions that work just like built in actions.
This file demonstrates how that's done.
_________________________________________________________________________________________
NOTES ABOUT FILES/MODULES:
You can create as many of these files as you like, but you must follow these rules:
(1) - All files you create must be placed in this user_actions folder.  *See note below.
(2) - The names of your files cannot begin with an underscore.
(3) - Your file should contain a class that extends UserActionsBase and that class should
      have the same name as the file (aka module) that contains it.  For example, this
      file's name is ExampleActions and the name of the class below is also
      ExampleActions.
Note that ClyphX_Pro uses sandboxing for importing from user-defined modules. So, if your
module contains errors, it will likely not be imported.
Also note that re-installing/updating Live and/or ClyphX Pro could cause files in this
user_actions folder to be removed.  For that reason, it is strongly recommended that you
back up your files in another location after creating or modifying them.  *See note below.
****** NEW IN V1.1.1 ******:
It is now possible to place your files in an alternate folder.  In this way, your files
will never be removed when re-installing/updating ClyphX Pro.  However, they can still
be removed when re-installing/updating Live, so the recommendation about backing up
files still holds.
To use the alternate folder:
(1) - Close Live.
(2) - In Live's MIDI Remote Scripts directory, create a folder named _user_actions
(3) - Copy the file named __init__.pyc from this user_actions folder and place it in the
      _user_actions folder you created.
(4) - Re-launch Live.
(5) - Create your files as described above, but place them in the _user_actions folder
      you created.
PLEASE NOTE: In order for the alternate folder to be used, the import statement in this
file (and all user action files) was changed.  So, if you'll be placing files you created
previously in the alternate folder, you'll need to change their import statements.
Instead of this:
from ..UserActionsBase import UserActionsBase
You should use this:
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
_________________________________________________________________________________________
NOTES ABOUT CLASSES:
As mentioned above, files you create should contain a class that extends UserActionsBase.
The class must implement a create_actions method, which is where you'll tell ClyphX_Pro
about the actions your class provides.  You can see this in the example class below.
There are several other useful methods that you can optionally override if you like:
(1) - on_track_list_changed(self) - This will be called any time the track list changes
      in Live.
(2) - on_scene_list_changed(self) - This will be called any time the scene list changes
      in Live.
(3) - on_selected_track_changed(self) - This will be called any time a track is selected
      in Live.
(4) - on_selected_scene_changed(self) - This will be called any time a scene is selected
      in Live.
(5) - on_control_surface_scripts_changed(self, scripts) - This will be called any time
      the list of control surface scripts changes in Live.  The scripts argument is a
      dict mapping the lower case names of scripts to the script objects themselves.
Additionally, there are a couple of other methods and attributes of UserActionsBase that
you should be aware of and that are demonstrated below:
(1) - self.song() - returns the current Live set object.
(2) - self.canonical_parent - returns the ControlSurface (parent) object that has loaded
      the ClyphX_Pro library.  Through this object, you can access two useful methods:
      (a) - log_message(msg) - Writes a message to Live's Log.txt file.
      (b) - show_message(msg) - Shows a message in Live's status bar.
Lastly, through the canonical_parent, you can access the core ClyphX Pro component, which
would allow you to trigger built in ClyphX Pro actions like so:
self.canonical_parent.clyphx_pro_component.trigger_action_list('metro ; 1/mute')
trigger_action_list accepts a single string that specifies the action list to trigger.
_________________________________________________________________________________________
NOTES ABOUT ACTIONS:
Your classes can create 4 types of actions each of which is slightly different, but all
have some common properties.
First of all, you define your actions in your class's create_actions method.  There is an
add method corresponding to each of the 4 types of actions you can create.  For example,
add_global_action(action_name, method) creates a global action.  All 4 add methods take
the same two arguments:
(1) - action_name - The single word, lowercase name to use when accessing the action from
      an X-Trigger. This name should not be the same as the name of any built in action.
(2) - method - The method in your class to call when the action has been triggered.
The methods for each type of action need to accept two arguments:
(1) - action_def - This is a dict that contains contents relevant to the type of action.
      The contents of this dict differs depending on the type of action, but always
      contains the following:
      (a) - xtrigger_is_xclip - A boolean indicating whether the action was triggered via
            an X-Clip.
      (b) - xtrigger - The X-Trigger that triggered the action.
(2) - args - Any arguments that follow the action name.  For example, in the case of
      'VOL RAMP 4 100', RAMP, 4 and 100 are all arguments following the action name (VOL).
      These arguments will be presented to you as a single string and will be converted to
      lower case unless one (or more) of the arguments is in quotes. Arguments in quotes
      are not converted in any way.
Note that ClyphX_Pro uses sandboxing for dispatching actions. So, if your method contains
errors, it will effectively be ignored.
_________________________________________________________________________________________
GLOBAL ACTIONS:
These actions don't apply to any particular object in Live.
Add method: add_global_action(action_name, method)
Additional action_def contents: No additional content.
_________________________________________________________________________________________
TRACK ACTIONS:
These actions apply to a track in Live and function just like Track Actions, so they'll be
called for each track that is specified.
Add method: add_track_action(action_name, method)
Additional action_def contents:
(1) - track - the track object to operate upon.
_________________________________________________________________________________________
DEVICE ACTIONS:
These actions apply to a device in Live and function just like Device Actions, so they'll
be called for each device that is specified.
Add method: add_device_action(action_name, method)
Additional action_def contents:
(1) - track - the track object containing the device.
(2) - device - the device object to operate upon.
Other notes, the action names for these actions are all preceded by 'user_dev'.  So, for
example, if you create a device action named 'my_action', its full name will be
'user_dev my_action'.  This allows your actions to apply to ranges of devices just like is
possible with Device Actions.  For example: 'user_dev(all) my_action'
_________________________________________________________________________________________
CLIP ACTIONS:
These actions apply to a clip in Live and function just like Clip Actions, so they'll
be called for each clip that is specified.
Add method: add_clip_action(action_name, method)
Additional action_def contents:
(1) - track - the track object containing the clip.
(2) - clip - the clip object to operate upon.
Other notes, the action names for these actions are all preceded by 'user_clip'.  So, for
example, if you create a clip action named 'my_action', its full name will be
'user_clip my_action'.  This allows your actions to apply to ranges of clips just like is
possible with Clip Actions.  For example: 'user_clip(all) my_action'
_________________________________________________________________________________________
"""

# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
# import numpy as np
# import Live
import time


# Your class must extend UserActionsBase.
class ExampleActions(UserActionsBase):
    """ ExampleActions provides some example actions for demonstration purposes. """

    # Your class must implement this method.
    def create_actions(self):
        """
        Here, we create 4 actions, each a different type:
        (1) - ex_global can be triggered via the name 'ex_global', which will call the
              method named global_action_example.
        (2) - ex_track can be triggered via the name 'ex_track', which will call the
              method named track_action_example.
        (3) - ex_device can be triggered via the name 'user_dev ex_device', which will
              call the method named device_action_example.
        (4) - ex_clip can be triggered via the name 'user_clip ex_clip', which will
              call the method named clip_action_example.
        """

        self.add_global_action('ex_global', self.global_action_example)
        self.add_track_action('ex_track', self.track_action_example)
        self.add_device_action('ex_device', self.device_action_example)
        self.add_clip_action('ex_clip', self.clip_action_example)
        self.add_global_action('test_global', self.global_action_test)
        # ---------- my user actions ----------
        self.add_clip_action('get_clip_length', self.get_clip_length)
        self.add_track_action('bpm_from_loop_new', self.set_new_bpm_from_loop_length_newVersion)
        self.add_track_action('get_track_index', self.get_track_index)
        self.add_global_action('get_track_number', self.get_track_number)
        self.add_global_action('count_playing_clips', self.count_playing_clips)
        self.add_track_action('play_from_last', self.play_counting_from_last_clip)
        self.add_track_action('set_simpler_slice', self.set_simpler_slice)
        self.add_track_action('plugin_preset_change', self.increment_plugin_preset)
        self.add_global_action('set_binklooper_beats', self.set_binklooper_beats)
        self.add_global_action('inc_binklooper_beats', self.increase_binklooper_beats)
        self.add_global_action('dec_binklooper_beats', self.decrease_binklooper_beats)
        self.add_global_action('autoset_binklooper_beats', self.autoset_binklooper_beats)
        self.add_global_action('navigate_tracks', self.navigate_in_music_tracks)
        self.add_global_action('navigate_clips', self.navigate_in_music_clips)
        self.add_global_action('del_simplers', self.delete_all_simpler_tracks)
        self.add_track_action('send_beat_to_main_scene', self.select_beat_and_paste_to_main_scene)
        self.add_track_action('play_or_stop', self.play_or_stop_first_clip)
        self.add_global_action('inc_bpm_from_loop_arg', self.increase_bpm_from_loop_arg)
        self.add_global_action('dec_bpm_from_loop_arg', self.decrease_bpm_from_loop_arg)
        self.add_global_action('new_loop_audio_track', self.new_loop_audio_track)
        self.add_global_action('launch_loop_tracks', self.launch_loop_tracks)
        self.add_track_action('stop_loop', self.stop_looper_track)
        self.add_global_action('initial_routing', self.reset_initial_routing)
        self.add_global_action('loopers_to_rec', self.route_loopers_into_rec_track)
        self.add_global_action('rec_to_loopers', self.route_rec_into_loopers)
        self.add_global_action('reset_session', self.reset_session)
        self.add_global_action('reset_loopers', self.reset_looper_tracks)
        self.add_global_action('play_rec_clip', self.play_rec_clip)
        self.add_track_action('tosimp', self.send_first_clip_to_simpler)
        self.add_global_action('set_last_simpler', self.set_last_simpler_track)
        self.add_global_action('reset_instru', self.reset_instru_tracks)
        self.add_global_action('switch_armed_instru', self.switch_armed_instru)
        self.add_global_action('bind_instru', self.bind_instru)
        self.add_global_action('bind_specific', self.bind_specific)
        self.add_global_action('bind_global', self.bind_global)
        self.add_global_action('navigate_beat', self.set_next_beat_to_first_scene)
        self.add_global_action('tiny_config', self.set_tinypad_configuration)
      #   self.add_global_action('see_looper_param', self.see_looper_param)



# ---------- INITIALIZING FUNCTION : DEF ALL USEFULL VARIABLES --------------
    def initialize_variables(self):
        """
        0 : tracks list
        1 : idx loop tracks
        2 : idx loop tracks full
        3 : nb loop_tracks 
        4 : idx measure tracks
        5 : idx measure tracks of full looper tracks
        6 : routing clip name
        7: idx INSTRU group
        8: idx instrument tracks
        9 : selected track
        10 : idx_selected track
        11: idx_loops_out_track
        """
        tracks=list(self.song().tracks)
        idx_loop_tracks = [i for i in range(len(tracks)) if "Loop" in tracks[i].name]
        idx_loop_full = [i+1 for i in range(len(idx_loop_tracks)) if list(tracks[idx_loop_tracks[i]].clip_slots)[0].has_clip]
        nb_loop_tracks = len(idx_loop_tracks)
        idx_measure_tracks = [i+nb_loop_tracks for i in idx_loop_tracks] # Assumption of measure tracks after loop tracks !! IT USED TO BE FOR ONLY FULL LOOPS; MIGHT HAVE PROBLEMS ONE DAY
        idx_measure_tracks_full = [i+nb_loop_tracks for i in idx_loop_full]
        routing_clip_name = list(tracks[0].clip_slots)[-2].clip.name # !!!! ATTENTION l'indice de routing clip name peut changer !!!!
        idx_instru_group = [i for i in range(len(tracks)) if "INSTRU" in tracks[i].name][0] # ATTENTION le nom peut changer
        idx_instru_tracks = [i for i in range(len(tracks)) if i > idx_instru_group and tracks[i].is_grouped is True] # ATTENTION la def peut changer
        sel_track = self.song().view.selected_track
        idx_sel_track = tracks.index(sel_track)
        idx_loops_out_track = [i for i in range(len(tracks)) if "LOOPS_OUT" in tracks[i].name][0]
        return tracks, idx_loop_tracks, idx_loop_full, nb_loop_tracks, idx_measure_tracks, idx_measure_tracks_full, routing_clip_name, idx_instru_group, idx_instru_tracks, sel_track, idx_sel_track, idx_loops_out_track
# ----------- END OF INITIALIZING FUNCTION ---------------------

#     def see_looper_param(self, action_def, _):
#         """"""
#         tracks, idx_instru_group=[self.initialize_variables()[i] for i in (0,7)]
#         instru_track = tracks[idx_instru_group]
#         instru_devices = list(instru_track.devices)
#         idx_looper_device = [i for i in range(len(instru_devices)) if instru_devices[i].name=="Looper"][0]
#         looper_device=instru_devices[idx_looper_device]
#         looper_parameters=list(looper_device.parameters)
#         param_names = [looper_parameters[i].name for i in range(len(looper_parameters))]
#         self.canonical_parent.show_message('param names %s' % param_names ) 
    

    def set_tinypad_configuration(self, action_def, arg):
        """as transport buttons are not supported for button binding in clyphx, this function changes the name of xclips with transport button functions depending on argument"""
        tracks=list(self.song().tracks)
        idx_tiny_transport_track = [i for i in range(len(tracks)) if "TinyTransports" in tracks[i].name ][0] # Carefull of not changing name of track
        tiny_transport_track=tracks[idx_tiny_transport_track]
        idx_tiny_notes_track=[i for i in range(len(tracks)) if "TinyNotes" in tracks[i].name ][0] # Carefull of not changing name of track
        tiny_notes_track=tracks[idx_tiny_notes_track]
        if arg == "0" :
            tiny_transport_track.clip_slots[0].clip.name="[] 1/CLIP(1) DEL"
            tiny_transport_track.clip_slots[1].clip.name="[] navigate_tracks"
            tiny_transport_track.clip_slots[2].clip.name="[] navigate_clips"
            tiny_transport_track.clip_slots[3].clip.name="SOME MACRO FUNCTION"
            tiny_transport_track.clip_slots[4].clip.name='[] "piano"/SEL ; "piano"/plugin_preset_change'
            tiny_transport_track.clip_slots[5].clip.name="[] switch_armed_instru"
            # ----
            tiny_notes_track.clip_slots[0].clip.name="[] inc_bpm_from_loop_arg 1"
            tiny_notes_track.clip_slots[1].clip.name="[] dec_bpm_from_loop_arg 1"
            tiny_notes_track.clip_slots[2].clip.name="[] inc_bpm_from_loop_arg 2"
            tiny_notes_track.clip_slots[3].clip.name="[] dec_bpm_from_loop_arg 2"
            tiny_notes_track.clip_slots[4].clip.name="[] inc_binklooper_beats"
            tiny_notes_track.clip_slots[5].clip.name="[] dec_binklooper_beats"
            tiny_notes_track.clip_slots[6].clip.name='[] "REC"/tosimp'
            tiny_notes_track.clip_slots[7].clip.name="[] autoset_binklooper_beats"
            tiny_notes_track.clip_slots[8].clip.name="[] SEL/send_beat_to_main_scene"
            tiny_notes_track.clip_slots[9].clip.name="[] (PSEQ) bind_instru ; bind_global ; bind_specific"
            tiny_notes_track.clip_slots[10].clip.name="[routing0] initial_routing"
            tiny_notes_track.clip_slots[11].clip.name="[routing1] loopers_to_rec"
           

        elif arg == "1":
            tiny_transport_track.clip_slots[0].clip.name='[] "INSTRU"/DEV("Looper") "State" "Overdub"'
            tiny_transport_track.clip_slots[1].clip.name='[] "INSTRU"/DEV("Looper") "Speed" < 21'
            tiny_transport_track.clip_slots[2].clip.name='[] "INSTRU"/DEV("Looper") "Speed" > 21'
            tiny_transport_track.clip_slots[3].clip.name='[] "INSTRU"/DEV("Looper") "State" "Record"'
            tiny_transport_track.clip_slots[4].clip.name='[] "INSTRU"/DEV("Looper") "State" "Stop"'
            tiny_transport_track.clip_slots[5].clip.name='[] "INSTRU"/DEV("Looper") "State" "Play"'
            # ----
            tiny_notes_track.clip_slots[0].clip.name="[] 2/play_or_stop"
            tiny_notes_track.clip_slots[1].clip.name="[] 2/stop_loop; 2/CLIP(1) DEL"
            tiny_notes_track.clip_slots[2].clip.name="[] 3/play_or_stop"
            tiny_notes_track.clip_slots[3].clip.name="[] 3/stop_loop; 3/CLIP(1) DEL"
            tiny_notes_track.clip_slots[4].clip.name="[] 4/play_or_stop"
            tiny_notes_track.clip_slots[5].clip.name="[] 4/stop_loop; 4/CLIP(1) DEL"
            tiny_notes_track.clip_slots[6].clip.name="[] 5/play_or_stop"
            tiny_notes_track.clip_slots[7].clip.name="[] 5/stop_loop; 5/CLIP(1) DEL"

            # tiny_notes_track.clip_slots[4].clip.name="[] inc_binklooper_beats"
            # tiny_notes_track.clip_slots[5].clip.name="[] dec_binklooper_beats"
            # tiny_notes_track.clip_slots[6].clip.name='[] "REC"/tosimp'
            # tiny_notes_track.clip_slots[7].clip.name="[] autoset_binklooper_beats"
            # tiny_notes_track.clip_slots[8].clip.name="[] SEL/send_beat_to_main_scene"
            # tiny_notes_track.clip_slots[9].clip.name="[] (PSEQ) bind_instru ; bind_global ; bind_specific"
            # tiny_notes_track.clip_slots[10].clip.name="[routing0] initial_routing"
            # tiny_notes_track.clip_slots[11].clip.name="[routing1] loopers_to_rec"
           

      #   elif arg == "2":
      #       tiny_transport_track.clip_slots[0].clip.name='[] "INSTRU"/DEV("Looper") "State" "Overdub"'
      #       tiny_transport_track.clip_slots[0].clip.name="[] 1/CLIP(1) DEL"
      #       tiny_transport_track.clip_slots[1].clip.name="[] navigate_tracks"
      #       tiny_transport_track.clip_slots[2].clip.name="[] navigate_clips"
      #       tiny_transport_track.clip_slots[3].clip.name='[] "INSTRU"/DEV("Looper") "State" "Record"'
      #       tiny_transport_track.clip_slots[4].clip.name='[] "INSTRU"/DEV("Looper") "State" "Stop"'
      #       tiny_transport_track.clip_slots[5].clip.name='[] "INSTRU"/DEV("Looper") "State" "Play"'

        self.canonical_parent.show_message('tiny name %s' % tiny_transport_track.clip_slots[0].clip.name ) 
      

    def set_next_beat_to_first_scene(self, action_def, _):
        """navigates in beats present in "Beats" track, sends the next one to first scene to be launched when button is used"""
        self.canonical_parent.show_message('louliloul00')
        tracks, idx_sel_track = [self.initialize_variables()[i] for i in (0,10)]
        self.canonical_parent.show_message('louliloul')
        self.canonical_parent.show_message('tracks %s ' % tracks)
        beats_track = [tracks[i] for i in range(len(tracks)) if "Beats" in tracks[i].name][0]
        self.canonical_parent.show_message('beats_track %s ' % beats_track)
        # -------------- find current beat name and where in the beats list it is --------------
        slots = list(beats_track.clip_slots)
        full_slots=[slots[i] for i in range(len(slots)) if slots[i].has_clip is True]
        self.canonical_parent.show_message('full slots : %s' % full_slots ) 
        idx_current_beat = [i for i in range(len(full_slots))[1:] if full_slots[i].clip.name == slots[0].clip.name][0]
        self.canonical_parent.show_message('idx current beat : %s' % int(idx_current_beat+1) ) 
        if idx_current_beat < len(full_slots)-1:
              idx_new_beat = idx_current_beat+1
        else:
              idx_new_beat = 1
      #  -------------- launches the function to the new beat, selected back previously selected track  --------------
        self.canonical_parent.clyphx_pro_component.trigger_action_list('"Beats"/SEL %s; "Beats"/send_beat_to_main_scene' % int(idx_new_beat+1))
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL' % int(idx_sel_track+1))
        self.canonical_parent.show_message('new beat in main scene %s ' % slots[idx_new_beat].clip.name)
      #   self.canonical_parent.clyphx_pro_component.trigger_action_list('"Beats"/CLIP(%s) SEL' % int(idx_current_beat+2))
      # self.canonical_parent.clyphx_pro_component.trigger_action_list('"Beats" send_beat_to_main_scene' )

    def bind_global(self, action_def, _):
        """global binding mode. binding linked to 1st param of the 4 musical tracks"""
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_1 "REC"/DEV("MainDev") B1 P1' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_2 "LOOPS_OUT"/DEV("MainDev") B1 P1' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_3 "INSTRU"/DEV("MainDev") B1 P1' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_4 "Beats"/DEV("MainDev") B1 P1' )
        self.canonical_parent.show_message('bind : global' ) 
      #   rename binding clip 
        tracks = list(self.song().tracks)
        list(tracks[0].clip_slots)[-3].clip.name = "bind : global"


    def bind_specific(self, action_def, _):
        """specific binding mode. binding linked to selected track"""
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_1 SEL/DEV("MainDev") B1 P1' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_2 SEL/DEV("MainDev") B1 P2' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_3 SEL/DEV("MainDev") B1 P3' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_4 SEL/DEV("MainDev") B1 P4' )
        self.canonical_parent.show_message('bind : specific' ) 
        #   rename binding clip 
        tracks = list(self.song().tracks)
        list(tracks[0].clip_slots)[-3].clip.name = "bind : specific"


    def bind_instru(self, action_def, _):
        """initial binding mode to instru parameters"""
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_1 "INSTRU"/DEV("MainDev") B1 P1' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_2 "INSTRU"/DEV("MainDev") B1 P2' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_3 "INSTRU"/DEV("MainDev") B1 P3' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('BIND ALESIS_KNOB_4 "INSTRU"/DEV("MainDev") B1 P4' )
        self.canonical_parent.show_message('bind : instru' ) 
        #   rename binding clip 
        tracks = list(self.song().tracks)
        list(tracks[0].clip_slots)[-3].clip.name = "bind : instru"

    def switch_armed_instru(self, action_def, _):
        """arm the instrument track next to that already armed, disarms all other"""
        tracks, idx_instru_group, idx_instru_tracks = [self.initialize_variables()[i] for i in (0,7,8)]
        idx_armed_instru = [idx_instru_tracks[i] for i in range(len(idx_instru_tracks)) if tracks[idx_instru_tracks[i]].arm]
        self.canonical_parent.show_message('idx instru armed : %s' % idx_armed_instru) 
        # Disarm current armed instru track and arms the next instru track (or arms the 1st instru track if the current armed track is the last instru)
        tracks[idx_armed_instru[0]].arm = False
        if idx_armed_instru[0]+1 <= max(idx_instru_tracks):
              tracks[idx_armed_instru[0]+1].arm = True
        else:
              tracks[idx_instru_tracks[0]].arm = True


    def reset_instru_tracks(self, action_def, _):
        """deleted all tracks from INSTRU group excepted piano"""
        tracks, idx_instru_group, idx_instru_tracks = [self.initialize_variables()[i] for i in (0,7,8)]
        for i in range(len(idx_instru_tracks)-2):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/DEL' % int(idx_instru_tracks[-1-i]+1) )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('"piano"/ARM ON')
      # 
    def set_last_simpler_track(self, action_def, _):
        """use set_simpler_slice on the most recent TOSIMP track"""
      #   track=action_def['track']
      #   idx_track = list(self.song().tracks).index(action_def['track'])
        tracks, idx_instru_group, idx_instru_tracks, idx_sel_track_init = [self.initialize_variables()[i] for i in (0,7,8,10)]
        self.canonical_parent.show_message('idx instru tracks : %s' % idx_instru_tracks) 
        idx_last_instru = idx_instru_tracks[-1]
        self.canonical_parent.show_message('idx last instru tracks : %s' % idx_last_instru) 
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/set_simpler_slice 4' % int(idx_last_instru+1) )

    def send_first_clip_to_simpler(self, action_def, _):
        """new slice track in INSTRU group, settings, naming it properly"""
        track=action_def['track']
        idx_track = list(self.song().tracks).index(action_def['track'])
        tracks, idx_instru_group, idx_instru_tracks, idx_sel_track_init = [self.initialize_variables()[i] for i in (0,7,8,10)]
        self.canonical_parent.show_message('pouet : ' ) 
        self.canonical_parent.show_message('idx instru tracks : %s' % idx_instru_tracks) 
        idx_last_instru = idx_instru_tracks[-1]
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL ; %s/CLIP(1) TOSIMP ; WAIT 10 ; %s/SEL' % (int(idx_last_instru+1),int(idx_track+1), int(idx_sel_track_init+1)) )
      #   self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/set_simpler_slice 4' % int(idx_last_instru+2) )
      #   self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL' % (int(idx_last_instru+1)),int(idx_track+1) )
      
    def play_rec_clip(self, action_def, _):
        """play top clip of rec. conditions on muting looper tracks depending on the state of routing"""
        tracks, idx_loop_tracks, name_routing_clip = [self.initialize_variables()[i] for i in (0,1,6)]
      #   name_muting_clip=list(tracks[0].clip_slots)[-2].clip.name
      #------------------- Conditions for Muting Loopers -------------
      # -------------- initial routing. Muting False -----------------
        if name_routing_clip[-1] == "0": 
              self.canonical_parent.show_message('routing 0. no mute') 
              for i in range(len(idx_loop_tracks)):
                    tracks[idx_loop_tracks[i]].mute=False 
      # ----------------- Loopers to rec. Si Clip Rec vide : muting false. Si Clip Rec plein : muting True -----------------
        elif name_routing_clip[-1] == "1":
              if list(tracks[0].clip_slots)[0].has_clip is False:
                    self.canonical_parent.show_message('routing 1 empty clip. no mute') 
                    for i in range(len(idx_loop_tracks)):
                          tracks[idx_loop_tracks[i]].mute=False 
              elif list(tracks[0].clip_slots)[0].has_clip is True:
                    self.canonical_parent.show_message('routing 1 full clip. mute') 
                    for i in range(len(idx_loop_tracks)):
                          tracks[idx_loop_tracks[i]].mute=True 
      # ---------- Play Rec clip ------------
        self.canonical_parent.clyphx_pro_component.trigger_action_list('1/PLAY 1')


    def reset_looper_tracks(self, action_def, _):
        """clear loop clips"""
        tracks, idx_loop_tracks, idx_measure_tracks = [self.initialize_variables()[i] for i in (0,1,4)]
        for i in range(len(idx_loop_tracks)):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(1) DEL' % int(idx_loop_tracks[i]+1) )
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP' % int(idx_measure_tracks[i]+1) )


    def reset_session(self, action_def, _):
        """No loop, no rec, MON in """
        self.canonical_parent.clyphx_pro_component.trigger_action_list('1/CLIP(1) DEL' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('reset_loopers' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('reset_instru' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('initial_routing' )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('bind_instru' )


    def route_rec_into_loopers(self, action_def, _): # Useless. better to do a Rec2 track, and then rec it back to rec1
        """Rec track in : piano, out : master, Monitor Auto. Loopers in : Rec, out : Master, Monitor off, ARM ON on loopers, ON on Rec """
        tracks=list(self.song().tracks)
        rec_track_name = tracks[0].name
        self.canonical_parent.clyphx_pro_component.trigger_action_list('1/IN "piano"; 1/OUT "Master"; 1/MON AUTO; 1/ARM ON' )
        idx_loop_tracks = [i for i in range(len(tracks)) if "Loop" in tracks[i].name or "Slice" in tracks[i].name] #Test with slice tracks
        for i in range(len(idx_loop_tracks)):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/IN "Rec"; %s/OUT "Master"; %s/MON OFF; %s/ARM ON' % (int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1)) )

#     def route_loopers_into_rec_track(self, action_def, _):
#         """Rec track in : piano, out : master, Monitor IN. Loopers in : piano, out : REC, Monitor off, ARM ON on loopers, ON on Rec """
#         tracks, idx_loop_tracks, routing_clip_name = [self.initialize_variables()[i] for i in (0,1,6)]
#         rec_track_name = tracks[0].name
#         self.canonical_parent.clyphx_pro_component.trigger_action_list('1/IN "piano"; 1/OUT "Master"; 1/MON AUTO; 1/ARM ON' ) 
#         for i in range(len(idx_loop_tracks)):
#               self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/IN "INSTRU"; %s/OUT "%s"; %s/MON OFF; %s/ARM ON' % (int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1),rec_track_name,int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1)) )
#               tracks[idx_loop_tracks[i]].mute=False 
#       # -------------------- modify routing clip name ---------------   
#         list(tracks[0].clip_slots)[-2].clip.name = routing_clip_name[0:-1] + "1"  
#         self.canonical_parent.show_message('%s' % routing_clip_name)   

    def route_loopers_into_rec_track(self, action_def, _):
        """Rec track in : piano, out : master, Monitor IN. Loopers in : piano, out : REC, Monitor off, ARM ON on loopers, ON on Rec """
        tracks, idx_loop_tracks, routing_clip_name, idx_loops_out_track = [self.initialize_variables()[i] for i in (0,1,6,11)]
        rec_track_name = tracks[0].name
        self.canonical_parent.clyphx_pro_component.trigger_action_list('1/IN "piano"; 1/OUT "Master"; 1/MON AUTO; 1/ARM ON' ) 
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/OUT "%s"; %s/MON IN; %s/ARM OFF' % (int(idx_loops_out_track+1),rec_track_name,int(idx_loops_out_track+1),int(idx_loops_out_track+1)) )
        tracks[idx_loops_out_track].mute=False 
      # -------------------- modify routing clip name ---------------   
        list(tracks[0].clip_slots)[-2].clip.name = routing_clip_name[0:-1] + "1"  
        self.canonical_parent.show_message('%s' % routing_clip_name)             
          

#     def reset_initial_routing(self, action_def, _):
#         """Rec track in : piano, out : master. Same for loopers. Monitor off for all"""
#         tracks, idx_loop_tracks, routing_clip_name = [self.initialize_variables()[i] for i in (0,1,6)]
#         for i in range(len(idx_loop_tracks)):
#               self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/IN "INSTRU"; %s/OUT "Master"; %s/MON OFF; %s/ARM ON' % (int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1),int(idx_loop_tracks[i]+1)) )
#               tracks[idx_loop_tracks[i]].mute=False 
#         self.canonical_parent.clyphx_pro_component.trigger_action_list('1/IN "INSTRU"; 1/OUT "Master"; WAIT 5; 1/MON OFF; 1/ARM ON' )
#         self.canonical_parent.clyphx_pro_component.trigger_action_list('"piano"/ARM ON' )
#         # -------------------- modify routing clip name ---------------          
#         list(tracks[0].clip_slots)[-2].clip.name = routing_clip_name[0:-1] + "0"  
#         self.canonical_parent.show_message('%s' % routing_clip_name)     
        
    def reset_initial_routing(self, action_def, _):
        """Rec track in : piano, out : master. Same for loopers. Monitor off for all"""
        tracks, idx_loop_tracks, routing_clip_name, idx_loops_out_track = [self.initialize_variables()[i] for i in (0,1,6,11)]
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/OUT "Master"; %s/MON IN; %s/ARM OFF' % (int(idx_loops_out_track+1),int(idx_loops_out_track+1),int(idx_loops_out_track+1)) )
        tracks[idx_loops_out_track].mute=False 
        self.canonical_parent.clyphx_pro_component.trigger_action_list('1/IN "INSTRU"; 1/OUT "Master"; WAIT 5; 1/MON OFF; 1/ARM ON' )
      #   self.canonical_parent.clyphx_pro_component.trigger_action_list('"piano"/ARM ON' )
        for i in range(len(idx_loop_tracks)):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/MUTE OFF' % (int(idx_loop_tracks[i]+1)) )

        # -------------------- modify routing clip name ---------------          
        list(tracks[0].clip_slots)[-2].clip.name = routing_clip_name[0:-1] + "0"  
        self.canonical_parent.show_message('%s' % routing_clip_name)     
        
   

    def stop_looper_track(self, action_def, arg):
        """stops looper and corresponding measure track """
        tracks=list(self.song().tracks)
        track = action_def['track']
        idx_track = list(self.song().tracks).index(action_def['track'])
        idx_loop_tracks = [i for i in range(len(tracks)) if "Loop" in tracks[i].name]
        nb_tracks = len(idx_loop_tracks)
        idx_measure_track = idx_track + nb_tracks 
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP' % int(idx_track+1))
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP' % int(idx_measure_track+1))




    def new_loop_audio_track(self, action_def, _):
        """ create loop in audio track, and corresponding midi clip in Measure track """
        tracks=list(self.song().tracks)
        measure_name_type = "Measures_"
        idx_loop_tracks = [i for i in range(len(tracks)) if "Loop" in tracks[i].name]
        nb_loop_tracks = len(idx_loop_tracks)
        idx_loop_target = 1
        bool_found_free_slot = False
        if idx_loop_target not in idx_loop_tracks :
              self.canonical_parent.show_message('idx 1 not in idx_loop_tracks') 
      # #  ---- get index of first empty loop track to fill ----
        for i in range(len(idx_loop_tracks)):
              if list(tracks[1+i].clip_slots)[0].has_clip is False : # add 1 to i because track[0] is rec
                    idx_loop_target = i+1
                    bool_found_free_slot = True
                    break
        idx_measure_track = idx_loop_target + nb_loop_tracks # Assumption of measure tracks right after loop tracks
        measure_name = tracks[idx_measure_track].name 
        if bool_found_free_slot is False:
              self.canonical_parent.show_message('need to make free slots !!') 
              return 
      # ---- copy and paste audio clip into empty loop track // CHANGE : directly rec in looper track ----
        self.canonical_parent.clyphx_pro_component.trigger_action_list('1/COPYCLIP 1')
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PASTECLIP 1' % int(idx_loop_target+1))
        list(tracks[idx_loop_target].clip_slots)[0].clip.warping = False
      #  ---- add dummy midi clip to measure track and adjust length  ----
        measure_clipslot = list(tracks[idx_measure_track].clip_slots)[0]
        loop_length = list(tracks[0].clip_slots)[0].clip.length # unit : beats
        if measure_clipslot.has_clip is False:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('"%s"/ADDCLIP 1' % measure_name)
        self.canonical_parent.clyphx_pro_component.trigger_action_list('"%s"/CLIP(1) LOOP START 0 ; "%s"/CLIP(1) LOOP END %s' % (measure_name, measure_name, loop_length))

    def launch_loop_tracks(self, action_def, _):
        """ after having created audio loop clips, launches clips and stops REC clip """
        tracks, idx_loop_tracks, idx_loop_full, nb_loop_tracks, idx_measure_tracks, idx_measure_tracks_full = [self.initialize_variables()[i] for i in (0,1,2,3,4,5)]
        if len(idx_loop_full) > 0:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('1/STOP')
              for i in range(len(idx_loop_full)):
                    if list(tracks[idx_measure_tracks_full[i]].clip_slots)[0].is_playing is False:
                          self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY 1' % int(idx_measure_tracks_full [i]+1))
        else:
              self.canonical_parent.show_message('no full looper track') 
         

    def decrease_bpm_from_loop_arg(self, action_def, args):
        """ decreases by 1 the beat numbers of bpm_from_loop argument or the measures number. if args = 1, measure number, if args = 2, beat numbers"""
        tracks=list(self.song().tracks)
        idx_bpm_ctrl_track = [i for i in range(len(tracks)) if "bpm" in tracks[i].name][0] 
        init_clip_name = list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name
      #   base_name="[] SEL/bpm_from_loop_new " # MIGHT CHANGE IF BPM FROM LOOP FUNCTION CHANGES
        base_name=init_clip_name[0:-3]
        length_arg=len(init_clip_name)-len(base_name)
        str_bpm_arg = init_clip_name[-length_arg:]
        list_bpm_arg=str_bpm_arg.split(' ')
        meas_arg = int(list_bpm_arg[0])
        time_arg=int(list_bpm_arg[1])
        if int(args) == 1: # modify measure numbers
              if meas_arg > 1:
                    meas_arg = meas_arg - 1
              else:
                    meas_arg=1
              self.canonical_parent.show_message('new meas arg %s' % meas_arg) 
              list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name = base_name + str(meas_arg) + ' ' + list_bpm_arg[1]
        elif int(args) == 2: # modify beat numbers
              if time_arg > 1:
                    time_arg = time_arg-1
              else:
                    time_arg=1
              self.canonical_parent.show_message('new time arg %s' % time_arg) 
              list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name = base_name + list_bpm_arg[0] + ' ' + str(time_arg)
        else:
              self.canonical_parent.show_message('wrong argument, need 1 or 2' )   
    
    def increase_bpm_from_loop_arg(self, action_def, args):
        """ increases by 1 the beat numbers of bpm_from_loop argument or the measures number. if args = 1, measure number, if args = 2, beat numbers """              
        tracks=list(self.song().tracks)
        idx_bpm_ctrl_track = [i for i in range(len(tracks)) if "bpm" in tracks[i].name][0] 
        init_clip_name = list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name
      #   base_name="[] SEL/bpm_from_loop_new " # MIGHT CHANGE IF BPM FROM LOOP FUNCTION CHANGES
        base_name=init_clip_name[0:-3]
        length_arg=len(init_clip_name)-len(base_name)
        str_bpm_arg = init_clip_name[-length_arg:]
        list_bpm_arg=str_bpm_arg.split(' ')
        meas_arg = int(list_bpm_arg[0])
        time_arg=int(list_bpm_arg[1])
        self.canonical_parent.show_message('coucou' )   
        if int(args) == 1: # modify measure numbers
              if meas_arg < 8:
                    meas_arg = meas_arg+1
              else:
                    meas_arg=8
              self.canonical_parent.show_message('new meas arg %s' % meas_arg) 
              list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name = base_name + str(meas_arg) + ' ' + list_bpm_arg[1]
        elif int(args) == 2: # modify beat numbers
              if time_arg < 11:
                    time_arg = time_arg+1
              else:
                    time_arg=11
              self.canonical_parent.show_message('new time arg %s' % time_arg) 
              list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name = base_name + list_bpm_arg[0] + ' ' + str(time_arg)
        else:
              self.canonical_parent.show_message('wrong argument, need 1 or 2' )   
      

    def play_or_stop_first_clip(self, action_def, _):
        """ plays or stops first clip of track, depending on the actual state """
        track = action_def['track']
        idx_track = list(self.song().tracks).index(action_def['track'])
        first_clipslot = list(track.clip_slots)[0]
        bool1=bool(first_clipslot.has_clip is False)
        nb_loop_tracks=self.initialize_variables()[3] 
        self.canonical_parent.show_message('bool1 : %s , nblooptrcks : %s' %  (bool1, nb_loop_tracks))
        if first_clipslot.has_clip is False:
              return
        else:
              if first_clipslot.is_playing:
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP ; %s/STOP' % (int(idx_track+1), int(idx_track+1+nb_loop_tracks)))
              else:
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY 1 ; %s/PLAY 1 ' % (int(idx_track+1), int(idx_track+1+nb_loop_tracks)))

        


    def select_beat_and_paste_to_main_scene(self, action_def, _):
        """ sends selected beat in beat track to scene 1 """
        track=action_def['track']
        bool1=bool("Beats" in track.name)
        self.canonical_parent.show_message('bool1 %s' % bool1 )
        if "Beats" in track.name:
              self.canonical_parent.show_message('beat track true ' )
              clipslots = list(track.clip_slots)
              idx_clip_selected = clipslots.index(self.song().view.highlighted_clip_slot)
              idx_clipslots_full = [i for i in range(len(clipslots)) if clipslots[i].has_clip]
              if idx_clip_selected in idx_clipslots_full:
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/COPYCLIP SEL ; SEL/PASTECLIP 1') 
            


    def delete_all_simpler_tracks(self, action_def, _):
        """ Deletes all Simpler tracks """
        tracks=list(self.song().tracks)
        string_music_track_names="Simpler"
        idx_simpler_tracks = [i for i in range(len(tracks)) if string_music_track_names in tracks[i].name]
        for i in range(len(idx_simpler_tracks)):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/DEL' % int(idx_simpler_tracks[i]+1)) 


    def navigate_in_music_clips(self, action_def, _):
        """ selects next clip in selected track if sel track is music track. other wise selects Rec track 1st clip """
        tracks=list(self.song().tracks)
        string_music_track_names=["test","REC","Beats","Bass"] # strings that will make a track considered as "music track"
        idx_music_tracks = []
        sel_track = self.song().view.selected_track
        idx_sel_track = tracks.index(sel_track)
        clipslots = list(sel_track.clip_slots)
        idx_clip_selected = clipslots.index(self.song().view.highlighted_clip_slot)
        idx_clipslots_full = [i for i in range(len(clipslots)) if clipslots[i].has_clip]
        # -------------- get indexes of music tracks ------------------
        for i in range(len(string_music_track_names)):
              idx_goodname = [item for item in range(len(tracks)) if string_music_track_names[i] in tracks[item].name]
              idx_music_tracks.extend(idx_goodname)
        idx_music_tracks.sort()
      #   # -------------- if music trck selected, select next clip. else, go back to Rec track, clip 1 ------------------
        if idx_sel_track in idx_music_tracks:
              # -------------- if last full clipslot selected, or empty slot selected, go back to 1st slot ---------
              if idx_clip_selected in idx_clipslots_full and idx_clip_selected is not idx_clipslots_full[-1]:
                    idx_clip_tosel=idx_clipslots_full[idx_clipslots_full.index(idx_clip_selected)+1]
              else:
                    idx_clip_tosel=idx_clipslots_full[0]
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/SEL %s' % int(idx_clip_tosel+1)) 
        else:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('1/SEL 1') 


    def navigate_in_music_tracks(self, action_def, _):
        """ selects next track among Simpler tracks, Rec track, Beat track, Bass track, Slice track """
        tracks=list(self.song().tracks)
        string_music_track_names=["REC","Beats","Slice","Bass","piano","LOOPS_OUT","Loop","INSTRU"] # strings that will make a track considered as "music track"
        idx_music_tracks = []
        sel_track = self.song().view.selected_track
        idx_sel_track = tracks.index(sel_track)
        # -------------- get indexes of music tracks ------------------
        for i in range(len(string_music_track_names)):
              idx_goodname = [item for item in range(len(tracks)) if string_music_track_names[i] in tracks[item].name]
              idx_music_tracks.extend(idx_goodname)
        idx_music_tracks.sort()
        for i in range(len(idx_music_tracks)):
              if idx_sel_track in idx_music_tracks and idx_sel_track is not idx_music_tracks[-1]: # if last track selected, go back to 1st track
                    new_sel_idx = idx_music_tracks[idx_music_tracks.index(idx_sel_track) + 1]
              else:
                    new_sel_idx = idx_music_tracks[0]
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL' % int(new_sel_idx+1)) 
        self.canonical_parent.show_message('sel track %s' % sel_track.name)
                
      
    def autoset_binklooper_beats(self, action_def, _):
        """ autosets the beat numbers of binklooper in 1st track according to parameter of bpmfromloop function """
        tracks=list(self.song().tracks)
        track_bink=list(self.song().tracks)[0]
        param_bink=list(track_bink.devices)[0].parameters
        idx_bpm_ctrl_track = [i for i in range(len(tracks)) if "bpm" in tracks[i].name][0] 
        self.canonical_parent.show_message('kikou' )
        init_clip_name = list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name
        list_bpm_arg=init_clip_name.split(' ')
        beat_arg=int(list_bpm_arg[-2])
        meas_arg=int(list_bpm_arg[-1])
        self.canonical_parent.show_message('beats %s' % type(param_bink[5].value)) #param[5] is loop length
        param_bink[5].value = beat_arg*meas_arg
        list(track_bink.clip_slots)[-1].clip.name = "Bink %d" % param_bink[5].value
        

    def decrease_binklooper_beats(self, action_def, _):
        """ decreases by 1 the beat numbers of binklooper in 1st track, changes its name to display new beat nb """
        track_bink=list(self.song().tracks)[0]
        param_bink=list(track_bink.devices)[0].parameters
        self.canonical_parent.show_message('beats %s' % type(param_bink[5].value)) #param[5] is loop length
        param_bink[5].value = min(1,param_bink[5].value-1)
        list(track_bink.clip_slots)[-1].clip.name = "Bink %d" % param_bink[5].value
        
    def increase_binklooper_beats(self, action_def, _):
        """ increases by 1 the beat numbers of binklooper in 1st track, changes its name to display new beat nb """
        track_bink=list(self.song().tracks)[0]
        param_bink=list(track_bink.devices)[0].parameters
        self.canonical_parent.show_message('beats %s' % type(param_bink[5].value)) #param[5] is loop length
        param_bink[5].value += 1
        list(track_bink.clip_slots)[-1].clip.name = "Bink %d" % param_bink[5].value 

    def set_binklooper_beats(self, action_def, args):
        """ sets beat numbers of binklooper in 1st track, changes its name to display new beat nb """
        track_bink=list(self.song().tracks)[0]
        param_bink=list(track_bink.devices)[0].parameters
        self.canonical_parent.show_message('beats %s' % type(param_bink[5].value)) #param[5] is loop length
        param_bink[5].value = int(args)
        list(track_bink.clip_slots)[-1].clip.name = "Bink %d" % int(args) 

    def increment_plugin_preset(self, action_def, args):
        """increment plugin preset index in program list"""
        track = action_def['track']   
        track_idx = list(self.song().tracks).index(action_def['track']) 
        self.canonical_parent.show_message('devices %s' % track.devices[0].chains[0].devices[0].name)
        if track.devices[0].chains[0].devices[0].selected_preset_index >= 4:
              track.devices[0].chains[0].devices[0].selected_preset_index = 0
        else:
              track.devices[0].chains[0].devices[0].selected_preset_index += 1 
    
    def set_simpler_slice(self, action_def, args):
        """set simpler in slice mode right after being created, split into 1 beat clip"""
        track = action_def['track']   
        track_idx = list(self.song().tracks).index(action_def['track']) 
        tracks, sel_track_init = [self.initialize_variables()[i] for i in (0,9)]
        self.canonical_parent.show_message('target track name : %s' % track.name)
        if track.name == "piano":
              self.canonical_parent.show_message('error : piano track targeted')
        else:
              idx_slice_tracks = [i for i in range(len(tracks)) if "Slice" in tracks[i].name]
              #   self.canonical_parent.show_message('idx slice tracks : %s' % idx_slice_tracks)
              slice_track_name = "Slice " + str(len(idx_slice_tracks))
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL' % int(track_idx+1))
            #   self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/ARM ON ; SEL/INSUB "Ch. 3"') # TO CHANGE IF NEEDED
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/INSUB "Ch. 3"') # TO CHANGE IF NEEDED
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/NAME "%s"' % slice_track_name)
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/DEV(1) SIMP PLAYMODE 3 ; SEL/DEV(1) SIMP WARP ON ; SEL/DEV(1) SIMP GATE OFF ; SEL/DEV(1) "Fade In" 40') #mode 3 = slice
              simpler=track.devices[0]
              simpler.sample.slicing_style = 1 # slice by beat
              simpler.sample.slicing_beat_division = int(args) # test
              simpler.sample.gain = 0.6 # => 8 db ?
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL' % int(sel_track_init+1))
      
        
    def play_counting_from_last_clip(self, action_def, args):
        """ plays the clip in position LAST-args of the selected track """
        track = action_def['track']    
        clipslots=list(track.clip_slots)
      #   list of indexes of clipslots where a clip is present 
        list_index_full = [i for i in range(len(clipslots)) if track.clip_slots[i].has_clip == True]
        idx_final = list_index_full[-1]-int(args)+1
        self.canonical_parent.show_message('idx final %s' % idx_final)
        self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/PLAY %s' % idx_final)
    
    def count_playing_clips(self, action_def, _):
        """ prints list of playing clips """
        bool_play=list()
        for i in range(0,len(list(self.song().tracks))):
              clip_slot = list(self.song().tracks)[i].clip_slots[0]
              if clip_slot.has_clip:
                    isplaying = clip_slot.clip.is_playing
              else:
                    isplaying = False
              bool_play.append(isplaying)
        self.canonical_parent.show_message('%s' % bool_play)
    
    def get_track_number(self, action_def, _):
        """ prints track number in the song """
        self.canonical_parent.show_message('ya qqun ')
        track_nb = len(list(self.song().tracks))
        self.canonical_parent.show_message('nb tracks : %s' % track_nb)
              
    def get_track_index(self, action_def, _):
        """ prints track index """
        track = action_def['track']   
        self.canonical_parent.show_message('ya qqun ')
        if track:
              # ------- get current track index  and print it
              original_track_index = list(self.song().tracks).index(action_def['track']) 
              self.canonical_parent.show_message('Track index : %s' % original_track_index) 
        else:
            self.canonical_parent.show_message('No track object')
        

    def set_new_bpm_from_loop_length_newVersion(self, action_def, args): 
          # Small delay if try to relaunch in this function directly ==> this fction only sets new bpm and measure length. need to launch after in other command
        """ sets new bpm from indicated clip length in selected track """
        args=args.split(' ') # we want args = [nb_measures nb_times_in_measure]
        tracks, idx_loop_tracks, nb_loop_tracks, idx_measure_tracks = [self.initialize_variables()[i] for i in (0,1,3,4)]
        sel_track = self.song().view.selected_track
        idx_sel_track = tracks.index(sel_track)
        clipslots = list(sel_track.clip_slots)
        idx_clipslots_full = [i for i in range(len(clipslots)) if clipslots[i].has_clip]
        bool_clipwasplaying=[]
        if len(idx_clipslots_full) > 0 and "Loop" in sel_track.name :
              # ----------- stop measure clips ----------
              for i in range(len(idx_loop_tracks)):
                    bool_clipwasplaying.append(bool(list(tracks[idx_measure_tracks[i]].clip_slots)[0].is_playing))
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP' % (int(idx_measure_tracks[i]+1)))
             #  --------------  get current bpm and calculate target bpm -----------------
              length_init = list(tracks[idx_sel_track+nb_loop_tracks].clip_slots)[0].clip.length # initial length based on corresponding measure length
              length_target = float(args[0])*float(args[1])  
              tempo_init = self.song().tempo
              odd_measures = [3,5,6,7,9,10,11] #List of args that will take into account time sig change
              if length_target in odd_measures:
                  #   time_sig_factor = 4/length_target # !!!!!!!! CA VA PAS CE FACTEUR !!!!!!!!!
                    time_sig_factor = 1 
              else:
                    time_sig_factor = 1              
              ratio_length_generic = length_target/length_init*time_sig_factor # can be used for all measure clips and for bpm
              tempo_target = tempo_init*ratio_length_generic
              self.canonical_parent.show_message('ancient BPM %s new BPM %s' % (tempo_init, tempo_target))    
            #  --------------  Change bpm -----------------
              self.canonical_parent.clyphx_pro_component.trigger_action_list('BPM %s' % tempo_target )

              # -------------------- adjusts length of Measure clips corresponding to existing Loop clips and relaunches them if previously playing ---------------
              for i in range(len(idx_loop_tracks)):
                    cliplength_init = tracks[idx_measure_tracks[i]].clip_slots[0].clip.length
                    if idx_loop_tracks[i] == idx_sel_track:
                          cliplength_target = length_target
                    else:
                          cliplength_target = cliplength_init*ratio_length_generic
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(1) LOOP START 0 ; %s/CLIP(1) LOOP END %.2f' % (int(idx_measure_tracks[i]+1),int(idx_measure_tracks[i]+1),cliplength_target))       
                  #   if bool_clipwasplaying[i]:
                        #   self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY 1' % (int(idx_measure_tracks[i]+1)))
        else:
            self.canonical_parent.show_message('No clip in Loop track or wrong track selected')
       #------- write which clips where playing in clip name --------
        idx_bpm_track = [i for i in range(len(tracks)) if "bpm" in tracks[i].name][0]
        nb_bpm_clipslots = len(list(tracks[idx_bpm_track].clip_slots))
        naming_clip = list(tracks[idx_bpm_track].clip_slots)[-2]
        name_bool_int = [int(bool_clipwasplaying[i]) for i in range(len(bool_clipwasplaying))]
        if naming_clip.has_clip is False:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/ADDCLIP %s' % (int(idx_bpm_track+1),int(nb_bpm_clipslots-1)))
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) NAME "%s"' % (int(idx_bpm_track+1),int(nb_bpm_clipslots-1),name_bool_int))
      

    def get_clip_length(self, action_def, _): 
        """ prints clip length """
        clip = action_def['clip']
        if clip: 
            self.canonical_parent.show_message('Clip length in beats : %s' % clip.length) 
            return clip.length
        else:
            self.canonical_parent.show_message('No clip object')

    def global_action_test(self, action_def, _):
        """ test """
        self.canonical_parent.show_message('X-Trigger is X-Clip=%s'
                                          % action_def['xtrigger_is_xclip'])


    def global_action_example(self, action_def, args):
        """ Logs whether the action was triggered via an X-Clip and shows 'Hello World'
        preceded by any args in Live's status bar. """
        self.canonical_parent.log_message('X-Trigger is X-Clip=%s'
                                          % action_def['xtrigger_is_xclip'])
        self.canonical_parent.show_message('%s: Hello World' % args)
        

    def track_action_example(self, action_def, args):
        """ Sets the volume and/or panning of the track to be the same as the master
        track.  This obviously does nothing if the track is the master track. """
        track = action_def['track']
        master = self.song().master_track
        if not args or 'vol' in args:
            track.mixer_device.volume.value = master.mixer_device.volume.value
        if not args or 'pan' in args:
            track.mixer_device.panning.value = master.mixer_device.panning.value

    def device_action_example(self, action_def, _):
        """ Resets all of the device's parameters and logs the name of the device.
        This method doesn't require any args so we use _ to indicate that. """
        device = action_def['device']
        if device:
            for p in device.parameters:
                if p.is_enabled and not p.is_quantized:
                    p.value = p.default_value
            self.canonical_parent.log_message('Reset device: %s' % device.name)

    def clip_action_example(self, action_def, args):
        """ Sets the name of the clip to the name specified in args.  We consider renaming
        the X-Clip that triggered this action an error and so we log that if it
        occurs. """
        clip = action_def['clip']
        if clip:
            if action_def['xtrigger'] != clip:
                clip.name = args
                self.canonical_parent.show_message('Clip renamed to %s' % args)
            else:
                self.canonical_parent.log_message('Error: Tried to rename X-Clip!')