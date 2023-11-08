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
        # ----------
        self.add_clip_action('get_clip_length', self.get_clip_length)
        self.add_track_action('bpm_from_loop_new', self.set_new_bpm_from_loop_length_newVersion)
        self.add_track_action('play_from_last', self.play_counting_from_last_clip)
        self.add_track_action('set_simpler_slice', self.set_simpler_slice)
        self.add_track_action('tosimp', self.send_first_clip_to_simpler)
        self.add_global_action('set_last_simpler', self.set_last_simpler_track)
      #   self.add_track_action('plugin_preset_change', self.increment_plugin_preset)
        self.add_global_action('set_binklooper_beats', self.set_binklooper_beats)
        self.add_global_action('inc_binklooper_beats', self.increase_binklooper_beats)
        self.add_global_action('dec_binklooper_beats', self.decrease_binklooper_beats)
        self.add_global_action('autoset_binklooper_beats', self.autoset_binklooper_beats)
        self.add_global_action('navigate_tracks', self.navigate_in_music_tracks)
        self.add_global_action('navigate_clips', self.navigate_in_music_clips)
        self.add_global_action('del_simplers', self.delete_all_simpler_tracks)
        self.add_global_action('inc_bpm_from_loop_arg', self.increase_bpm_from_loop_arg)
        self.add_global_action('dec_bpm_from_loop_arg', self.decrease_bpm_from_loop_arg)
        self.add_global_action('initial_routing', self.reset_initial_routing)
        self.add_global_action('loopers_to_rec', self.route_loopers_into_rec_track)
        self.add_global_action('rec_to_loopers', self.route_rec_into_loopers)
        self.add_global_action('reset_session', self.reset_session)
        self.add_global_action('reset_loopers', self.reset_looper_tracks)
        self.add_global_action('play_rec_clip', self.play_rec_clip)
        self.add_global_action('reset_instru', self.reset_instru_tracks)
        self.add_global_action('switch_armed_instru', self.switch_armed_instru)
        self.add_global_action('tiny_config', self.set_tinypad_configuration)
        self.add_global_action('bpm_1bar_clip', self.set_bpm_from_1bar_clip)
        self.add_global_action('adjust_length_beatmidi', self.adjust_length_beatmidi)
        self.add_global_action('switch_beatmidi', self.switch_beatmidi)
        self.add_global_action('adjust_length_loopclips', self.adjust_length_loopclips)
        self.add_global_action('adjust_length_loopclips_new', self.adjust_length_loopclips_new)
        self.add_global_action('switch_rec_free_sync', self.switch_rec_free_sync)
        self.add_global_action('play_recloop', self.play_recloop)
        self.add_global_action('qtzornot_loopers', self.qtzornot_loopers)
        self.add_global_action('qtzornot_loopers2', self.qtzornot_loopers2)
        self.add_global_action('reset_routing_new', self.reset_routing_new)
        self.add_track_action('new_beats_fromdump', self.new_beats_from_dump)
        self.add_global_action('duplicate_and_transpose', self.duplicate_and_transpose)
        self.add_track_action('tell_param_names', self.tell_param_names)
        self.add_track_action('activ_dlo', self.activate_DLo_buttons)
        self.add_global_action('switch_clear_undo', self.switch_DLobuttons_clear_undo)
        self.add_track_action('color_sel_looper', self.color_looper_cmd_track)
        self.add_global_action('rec_sel_looper', self.rec_sel_looper)
        self.add_track_action('clip_from_bpmarg', self.create_clip_from_bpm_arg)
        self.add_global_action('ovd_allinst', self.ovd_allinst)
        self.add_global_action('play_all_loopers', self.play_all_loopers)
        self.add_global_action('stop_all_loopers', self.stop_all_loopers)
        self.add_track_action('adjust_loopersrec', self.adjust_loopersrec_ABC)




# ---------- INITIALIZING FUNCTION : DEF ALL USEFULL VARIABLES --------------
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
        12 : idx_beats_group
        13 : idx_bpm_ctrl_track
        14 : live sample frames parameter
        15 : names_beats_midi
        16 : idx_cmdloop_tracks
        17 : idx_recloop_track
        18 : idx_dump_group
        """
        tracks=list(self.song().tracks)
        idx_loop_tracks = [i for i in range(len(tracks)) if "Looper" in tracks[i].name]
        idx_loop_full = [i+1 for i in range(len(idx_loop_tracks)) if list(tracks[idx_loop_tracks[i]].clip_slots)[0].has_clip]
        nb_loop_tracks = len(idx_loop_tracks)
      #   ----- NO MEASURE TRACKS ANYMORE  --------- 
        idx_measure_tracks = []
        idx_measure_tracks_full = []
      #   idx_measure_tracks = [i+nb_loop_tracks for i in idx_loop_tracks] # Assumption of measure tracks after loop tracks !! IT USED TO BE FOR ONLY FULL LOOPS; MIGHT HAVE PROBLEMS ONE DAY
      #   idx_measure_tracks_full = [i+nb_loop_tracks for i in idx_loop_full]
        routing_clip_name = [slot for slot in list(tracks[0].clip_slots) if slot.has_clip and "routing" in slot.clip.name][0].clip.name
      #   routing_clip_name = list(tracks[0].clip_slots)[-4].clip.name # !!!! ATTENTION l'indice de routing clip name peut changer !!!!
        idx_instru_group = [i for i in range(len(tracks)) if "INSTRU" in tracks[i].name][0] # ATTENTION le nom peut changer
        idx_beats_group = [i for i in range(len(tracks)) if "GrpBeet" in tracks[i].name] # ATTENTION le nom peut changer
        if len(idx_beats_group) > 0:
                idx_beats_group = idx_beats_group[0]
        if len(idx_beats_group) > 0:
             idx_instru_tracks = [i for i in range(len(tracks)) if i > idx_instru_group and i < idx_beats_group and tracks[i].is_grouped is True] # ATTENTION la def peut changer
        else:
             idx_instru_tracks = [i for i in range(len(tracks)) if i > idx_instru_group and tracks[i].is_grouped is True] # ATTENTION la def peut changer
        sel_track = self.song().view.selected_track
        idx_sel_track = tracks.index(sel_track)
        idx_loops_out_track = [i for i in range(len(tracks)) if "LOOPS_OUT" in tracks[i].name][0]
        idx_bpm_ctrl_track = [i for i in range(len(tracks)) if "bpm" in tracks[i].name][0]
        live_sample_frames = 44100 # CAN BE CHANGED
        names_beats_midi = ['beatardeche',"FunkyClyphX","beatrebou","ThugBeat"] # parts of chain simpler names in beats midi drumracks !! NO CAPITAL LETTER IN NAMESBEATS
        idx_cmdloop_tracks = [i for i in range(len(tracks)) if "CmdLoop" in tracks[i].name]
        idx_recloop_track=[i for i in range(len(tracks)) if "RECLOOP" in tracks[i].name][0]
        idx_dump_group=[i for i in range(len(tracks)) if "DUMP" in tracks[i].name]
        if len(idx_dump_group) > 0:
              idx_dump_group = idx_dump_group[0]

        return tracks, idx_loop_tracks, idx_loop_full, nb_loop_tracks, idx_measure_tracks, idx_measure_tracks_full, routing_clip_name, idx_instru_group, idx_instru_tracks, sel_track, idx_sel_track, idx_loops_out_track, idx_beats_group, idx_bpm_ctrl_track, live_sample_frames, names_beats_midi, idx_cmdloop_tracks, idx_recloop_track, idx_dump_group
# ----------- END OF INITIALIZING FUNCTION ---------------------
    

    def adjust_loopersrec_ABC(self, action_def, args): # A TESTER
        """pastes right rec clip for rec scenes 8-15 in looper tracks"""
        self.canonical_parent.show_message('pouet00') 
        tracks, idx_loop_tracks, idx_bpm_ctrl_track = [self.initialize_variables()[i] for i in (0,1,13)]
        self.canonical_parent.show_message('pouet0') 
        action_track = action_def['track']   
        actiontrack_idx = list(self.song().tracks).index(action_def['track']) 
        self.canonical_parent.show_message('beats + args : %s' % str("beats "+args)) 
        goodslots_idx = [idx for idx in range(len(list(action_track.clip_slots))) if list(action_track.clip_slots)[idx].has_clip and args.upper() == list(action_track.clip_slots)[idx].clip.name.split(' ')[-1] and idx > 20] # condition idx > 20 to be sure we dont count the active rec buttons
        self.canonical_parent.show_message('args : .%s. goodslots %s' % (args,goodslots_idx))
      #   self.canonical_parent.show_message('sc 25 last word %s' % list(action_track.clip_slots)[25].clip.name.split(' ')) 
        for i in range(len(goodslots_idx)):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/COPYCLIP %s ; %s/PASTECLIP %s' % (int(actiontrack_idx+1), int(goodslots_idx[i]+1), int(actiontrack_idx+1), int(i+8))) # rec clips start at scene 8


    def stop_all_loopers(self, action_def, _): 
        """finds loopers idx and plays all (clip 5)"""
        idx_loop_tracks = self.initialize_variables()[1]
        str_idx = ''
        for i in range(len(idx_loop_tracks)):
              str_idx += str(int(idx_loop_tracks[i]+1))
              if i < len(idx_loop_tracks)-1:
                    str_idx += ','
        self.canonical_parent.show_message('str : %s' % str_idx) 
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY 5' % (str_idx))
         
    def play_all_loopers(self, action_def, _): 
        """finds loopers idx and plays all (clip 3)"""
        idx_loop_tracks = self.initialize_variables()[1]
        str_idx = ''
        for i in range(len(idx_loop_tracks)):
              str_idx += str(int(idx_loop_tracks[i]+1))
              if i < len(idx_loop_tracks)-1:
                    str_idx += ','
        self.canonical_parent.show_message('str : %s' % str_idx) 
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY 3' % (str_idx))
         
    def ovd_allinst(self, action_def, _): 
        """activates session record in order to record automation for all inst first clip. disables REC and OUTPUT monitoring while recording allInst, enables it afterwards"""
        self.canonical_parent.show_message('coucou') 
        self.canonical_parent.show_message('ovd_status : %s' % self.song().session_record) 
        if self.song().session_record == False:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('"REC","OUTPUTMASTER"/ARM OFF')
              self.song().session_record = True
        elif self.song().session_record == True:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('reset_routing_new')
              self.song().session_record = False
        self.canonical_parent.show_message('ovd_status new : %s' % self.song().session_record) 
      


    def create_clip_from_bpm_arg(self, action_def, _): 
        """launches first clip (rec) of the selected track if it is a looper track"""
        all_tracks = self.initialize_variables()[0]
        action_track = action_def['track']   
        actiontrack_idx = list(self.song().tracks).index(action_def['track']) 
        self.canonical_parent.show_message('action track idx : %s' % actiontrack_idx) 
        bpm_clip = list(all_tracks[0].clip_slots)[-4].clip
        bpmclip_name_split = bpm_clip.name.split(' ')
        meas_arg = bpmclip_name_split[1]
      #   beat_arg = int(bpmclip_name_split[2])
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(1) DEL' % (int(actiontrack_idx+1)))
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/ADDCLIP 1 %s' % (int(actiontrack_idx+1),meas_arg))
        list(action_track.clip_slots)[0].clip.name = meas_arg + ' bars clip'
        self.canonical_parent.show_message('meas : %s ' % meas_arg) 



    def rec_sel_looper(self, action_def, _): 
        """launches first clip (rec) of the selected track if it is a looper track""" 
        sel_track, idx_sel_track = [self.initialize_variables()[i] for i in (9,10)]
        if "Looper" in sel_track.name:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY 2' % int(idx_sel_track+1))
        else:
              self.canonical_parent.show_message('wrong track selected')


    def color_looper_cmd_track(self, action_def, args): 
        """colorizes in bright the command track corresponding to the selected looper""" 
        self.canonical_parent.show_message('coucou3')
      #   tracks, idx_cmdloop_tracks = [self.initialize_variables()[i] for i in (0,16)]
        tracks=list(self.song().tracks)
        action_track = action_def['track']
        actiontrack_idx = list(self.song().tracks).index(action_def['track']) 
        idx_LP_tracks=[i for i in range(len(tracks)) if "LP" in tracks[i].name]
        for i in range(len(idx_LP_tracks)):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(1-4) COLOR 2' % int(idx_LP_tracks[i]+1))
        if "LP" in action_track.name and len(args) == 0:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(1-4) COLOR 32' % int(actiontrack_idx+1))
              self.canonical_parent.show_message('coucoucoucou')


    def switch_DLobuttons_clear_undo(self, action_def, _): 
        """activates clear, clear_all, undo, or undo_all buttons from DLo Max Device. plus 3d mode to use x2 and :2 functions of looper""" # MARCHE SI DLO CLIPS IN LP1 AND LP2 TRACKS
        self.canonical_parent.show_message('coucou3')
        tracks=list(self.song().tracks)
        idx_LP_tracks=[i for i in range(len(tracks)) if "LP" in tracks[i].name]
        for i in (0,1):
              LPtrack = tracks[idx_LP_tracks[i]]
              LPslots = list(LPtrack.clip_slots)
              self.canonical_parent.show_message('len LPslots %s' % len(LPslots))
              idx_dloclips = [j for j in range(len(LPslots)) if LPslots[j].has_clip and bool("[clear" in LPslots[j].clip.name or "[undo" in LPslots[j].clip.name or "[x2" in LPslots[j].clip.name or "[:2" in LPslots[j].clip.name)][0]
              self.canonical_parent.show_message('iddx dlos %s' % idx_dloclips)
              string_inbrackets = (LPslots[idx_dloclips].clip.name.split("[")[1]).split("]")[0]
              self.canonical_parent.show_message('string brackets %s' % string_inbrackets)
              if "[clear" in LPslots[idx_dloclips].clip.name:
                    LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace("clear","undo")
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('"LP1","LP2"/CLIP(%s) COLOR 40' % int(idx_dloclips+1))
              elif "[undo" in LPslots[idx_dloclips].clip.name:
                    LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace("LP1","LP2")
                    if i == 0:
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace(string_inbrackets,":2",1)
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace(string_inbrackets,"clear")
                    elif i == 1:
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace(string_inbrackets,"x2",1)
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace(string_inbrackets,"undo")
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('"LP1","LP2"/CLIP(%s) COLOR 20' % int(idx_dloclips+1))
              elif "[x2" in LPslots[idx_dloclips].clip.name or "[:2" in LPslots[idx_dloclips].clip.name:
                    if i == 0:
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace(string_inbrackets,"clear")
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace("undo","clear")
                    elif i == 1:
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace(string_inbrackets,"clear_all")
                          LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace("undo","clear_all")
                    LPslots[idx_dloclips].clip.name = LPslots[idx_dloclips].clip.name.replace("LP2","LP1")
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('"LP1","LP2"/CLIP(%s) COLOR 2' % int(idx_dloclips+1))

    def activate_DLo_buttons(self, action_def, args): 
        """activates clear, clear_all, undo, or undo_all buttons from DLo Max Device"""
        action_track = action_def['track']
        actiontrack_idx = list(self.song().tracks).index(action_def['track']) 
        devices = list(action_track.devices)
        param_nb = 0
        if len(args) == 0:
              self.canonical_parent.show_message('args problem')
        if args == 'clear':
              param_nb = 1
        elif args == 'clear_all':
              param_nb = 2
        elif args == 'undo':
              param_nb = 6
        elif args == 'undo_all':
              param_nb = 7
        else:
              self.canonical_parent.show_message('args problem')
        self.canonical_parent.show_message('coucou3')
        dlo_dev = devices[0]
      #   dlo_dev.parameters[param_nb].name
        self.canonical_parent.show_message('type args : %s' % type(args))
        self.canonical_parent.show_message(dlo_dev.parameters[param_nb].name)
        self.canonical_parent.show_message('param value : %s' % dlo_dev.parameters[param_nb].value)
        dlo_dev.parameters[param_nb].value = True



    def tell_param_names(self, action_def, args): 
        """bla"""
        action_track = action_def['track']
        actiontrack_idx = list(self.song().tracks).index(action_def['track']) 
        devices = list(action_track.devices)
        idx_device = int(args)
        interest_device = devices[idx_device]
        text_names = ''
        for i in range(len(interest_device.parameters)):
              text_names += ('P%s : %s / ' % (int(i+1), interest_device.parameters[i].name))
        self.canonical_parent.show_message(text_names)
      #   self.canonical_parent.show_message('%s' % interest_device.parameters[1].is_quantized)


    def qtzornot_loopers2(self, action_def, _): 
        """switches between quantized or not quantized clips"""
        tracks, idx_cmdloop_tracks = [self.initialize_variables()[i] for i in (0,16)]
        clip_name = "" 
        for i in range(len(idx_cmdloop_tracks)):
            for j in range(4):
                    idx_track = int(idx_cmdloop_tracks[i]) 
                    clip_name = str(list(tracks[idx_track].clip_slots)[j].clip.name)
                    self.canonical_parent.show_message('track %s, clip %s, name %s' % (int(idx_track+1),int(j+1),clip_name))

                    if "QTZ" in clip_name and "OVD" not in clip_name:
                        #  and "OVD" not in clip_name
                          clip_name = clip_name.replace("/PLAYQ 1 BAR","/PLAY")
                          clip_name = clip_name.replace("QTZ","")
                          self.canonical_parent.show_message('%s' % clip_name)
                          self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) NAME "%s"' % (int(idx_track+1),int(j+1),clip_name))
                    elif "QTZ" not in clip_name and "OVD" not in clip_name:
                          clip_name = clip_name.replace("/PLAY","/PLAYQ 1 BAR")
                          clip_name = clip_name.replace("]","QTZ]")
                          self.canonical_parent.show_message('%s' % clip_name)
                          self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) NAME "%s"' % (int(idx_track+1),int(j+1),clip_name))
                        #   self.canonical_parent.clyphx_pro_component.trigger_action_list('')
            #   self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) NAME "%s"' % (int(idx_track+1),int(j+1),clip_name))
            #   self.canonical_parent.show_message('%s' % clip_name)
   

    def duplicate_and_transpose(self, action_def, _): 
        tracks, idx_recloop_track = [self.initialize_variables()[i] for i in (0,17)] 
        self.canonical_parent.show_message('8 new beats pasted' )
        for i in range(11):
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/COPYCLIP 1' % int(idx_recloop_track+1))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PASTECLIP %s' % (int(idx_recloop_track+1),int(i+2)))
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) SEMI %s' % (int(idx_recloop_track+1),int(i+2),int(i+1)))


    def new_beats_from_dump(self, action_def, _): 
        """copy beats, SC, and fills from DUMP group and pastes it to effective beatGroup"""
        tracks, idx_beats_group, idx_dumpgroup = [self.initialize_variables()[i] for i in (0,12,18)] 
        # --------- read Dump info clip to know which scenes to copy in the dump group ----------
        # ---------- CAREFULL: DUMP INFO CLIP MUST BE IN SAME TRACK AS THE CURRENT USER ACTION CLIP -----------
        track = action_def['track']   
        track_idx = list(self.song().tracks).index(action_def['track']) 
        track_clipslots = list(track.clip_slots)
        idx_dmpinfo = [i for i in range(len(track_clipslots)) if track_clipslots[i].has_clip and "DMPINFO" in track_clipslots[i].clip.name][0]
        dmpinfo_name = track_clipslots[idx_dmpinfo].clip.name
        dmpinfo_split = dmpinfo_name.split(' ')
        dmpinfo_split_last = int(dmpinfo_split[-1])
        idx_scenes_dump = [i+(dmpinfo_split_last-1)*8 for i in range(8)]
      #   self.canonical_parent.show_message('idx_scenes_dump : %s' % idx_scenes_dump)
        # --------- copy and paste clips from dump to effective beatgroup ---------
        idx_copy = [idx_dumpgroup+1, idx_dumpgroup+2, idx_dumpgroup+3, idx_dumpgroup+4, idx_dumpgroup+5]
        idx_paste = [idx_beats_group+1, idx_beats_group+2, idx_beats_group+3, idx_beats_group+4, idx_beats_group+5]
        for i in range(len(idx_copy)):
              for j in range(len(idx_scenes_dump)):
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/COPYCLIP %s' % (int(idx_copy[i]+1),int(idx_scenes_dump[j]+1)))
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PASTECLIP %s' % (int(idx_paste[i]+1),int(j+1)))
      #   ------------ rename Dump info clip : CAREFULL: DUMP INFO CLIP MUST BE IN SAME TRACK AS THE CURRENT USER ACTION CLIP  --------------
        dmpinfo_split_last += 1
        if dmpinfo_split_last > 3:
              dmpinfo_split_last = 1
        track_clipslots[idx_dmpinfo].clip.name = ' '.join(dmpinfo_split[:-1]) + " " + str(dmpinfo_split_last)
        self.canonical_parent.show_message('8 new beats pasted' )

        
    def reset_routing_new(self, action_def, _): 
        """arms right tracks in case wrong manipulation has been made : unarms all, then arms REC (and mute it) and arms first track of Instru Group"""
        idx_instru_group = self.initialize_variables()[7]
        self.canonical_parent.show_message('coucou0')

        self.canonical_parent.clyphx_pro_component.trigger_action_list('all/ARM OFF ; "OUTPUTMASTER","VOIX"/ARM ON')
        self.canonical_parent.clyphx_pro_component.trigger_action_list('1/IN "INSTRU" ; 1/OUT "Master" ; WAIT 5 ; 1/MON AUTO ; 1/ARM ON ; 1/MUTE ON')
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/ARM ON' % int(idx_instru_group+2))


    def qtzornot_loopers(self, action_def, _): 
        """switches between quantized or not quantized clips"""
        tracks, idx_cmdloop_tracks = [self.initialize_variables()[i] for i in (0,16)]
        self.canonical_parent.show_message('coucou')
        for i in range(len(idx_cmdloop_tracks)):
              idx = int(idx_cmdloop_tracks[i] + 1) 
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/COPYCLIP 10 ; %s/PASTECLIP 9 ; %s/COPYCLIP 1 ; %s/PASTECLIP 10 ; %s/COPYCLIP 9 ; %s/PASTECLIP 1' % (idx,idx,idx,idx,idx,idx))
   

    def play_recloop(self, action_def, _): # A TESTER. NEED TO SET IT AS A CLIP ACTION
        """plays first recloop clip and stops loopers if it is the second time this function is used"""
      #   clip = action_def['clip']
        tracks, idx_loop_tracks, idx_recloop_track, idx_bpm_ctrl_track = [self.initialize_variables()[i] for i in (0,1,17,13)]
        str_loopertracks_idx=str([i+1 for i in idx_loop_tracks])[1:-1]
        recloop_track = tracks[idx_recloop_track]
        recloop_slots=list(recloop_track.clip_slots)
        idx_mpd_track = [i for i in range(len(tracks)) if "MPD" == tracks[i].name][0]
        mpd_track = tracks[idx_mpd_track]
        self.canonical_parent.show_message('mpd track %s' % mpd_track)
        mpd_slots= list(mpd_track.clip_slots)
        self.canonical_parent.show_message(' len mpd_slots %s' % len(mpd_slots))
        idx_action_clip = [i for i in range(len(mpd_slots)) if mpd_slots[i].has_clip and "recloop_playSync" in mpd_slots[i].clip.name][0]
        self.canonical_parent.show_message('idx_action_clip %s' % idx_action_clip)
        init_clip_name = list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name
        list_bpm_arg=init_clip_name.split(' ')
        beat_arg=int(list_bpm_arg[-1])
        meas_arg=int(list_bpm_arg[-2])
        self.canonical_parent.show_message('beat arg %s' % beat_arg)
        if recloop_slots[0].has_clip:
               self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/PLAY 1 ; %s/PLAY 5' % (int(idx_recloop_track+1),str_loopertracks_idx))
               self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/ARM OFF' % (int(idx_recloop_track+1)))     
        else:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/CLIP(%s) LOOP END %s.1.1' % (int(idx_mpd_track+1),int(idx_action_clip+1),int(meas_arg+1)))
              self.canonical_parent.show_message('idx recloop track %s' % idx_recloop_track)
              self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/ARM ON ; %s/PLAY 1' % (int(idx_recloop_track+1),int(idx_recloop_track+1)))

    
    def switch_rec_free_sync(self, action_def, _): # A TESTER
        """switches cmd clyphx command from free looper rec to sync rec"""
        tracks, idx_cmdloop_tracks = [self.initialize_variables()[i] for i in (0,16)]
        info_rec_clip = list(tracks[0].clip_slots)[18].clip
        info_rec = info_rec_clip.name.split(" ")[-1]
        self.canonical_parent.show_message('info rec : %s' % info_rec)
        if info_rec == "Sync" :
              for i in range(len(idx_cmdloop_tracks)):
                    new_recclip_name = '[Rec] ' + str(int(idx_cmdloop_tracks[i]+1-5)) + '/DEV("Looper") "State" 1'
                    self.canonical_parent.show_message('new name : %s' % new_recclip_name)
                    cmdtrack = tracks[idx_cmdloop_tracks[i]]
                    self.canonical_parent.show_message('old name : %s' % list(cmdtrack.clip_slots)[1].clip.name)
                    list(cmdtrack.clip_slots)[0].clip.name = new_recclip_name
              info_rec_clip.name = ' '.join(info_rec_clip.name.split(" ")[:-1]) + " Free"
        elif info_rec == "Free" :
              self.canonical_parent.show_message('kikou')
              for i in range(len(idx_cmdloop_tracks)):
                    new_recclip_name = '[Rec] ' + str(int(idx_cmdloop_tracks[i]+1-5)) + '/PLAY 2'
                    cmdtrack = tracks[idx_cmdloop_tracks[i]]
                    list(cmdtrack.clip_slots)[0].clip.name = new_recclip_name
              info_rec_clip.name = ' '.join(info_rec_clip.name.split(" ")[:-1]) + " Sync" 




       
        

    def adjust_length_loopclips_new(self, action_def, args): # A TESTER
        """chooses the right rec clip with the right automation looper enveloppe"""
        tracks, idx_loop_tracks, idx_bpm_ctrl_track = [self.initialize_variables()[i] for i in (0,1,13)]
      #   idx_loop_tracks = [1,2,3,4] # EN DUR ATTENTION
        init_clip_name = list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name
        list_bpm_arg=init_clip_name.split(' ')
        beat_arg=list_bpm_arg[-1]
        meas_arg=list_bpm_arg[-2]
        total_beats_asked = str(int(beat_arg)*int(meas_arg))
        all_clip_names = []
        all_names_dico={}
        good_name_1 = "rec " + meas_arg + " " + beat_arg
        good_name_2 = "rec " + total_beats_asked + " beats"
        good_track_idx = 0
        good_slot_idx = 0
        str_loopertracks_idx=str([i+1 for i in idx_loop_tracks])[1:-1]
        for i in range(len(idx_loop_tracks)):
            # --- read and find got rec name ---
              idx = idx_loop_tracks[i]
              track_loop = tracks[idx]
              clipslots = list(track_loop.clip_slots)
            #   self.canonical_parent.show_message('coucou')
            #   self.canonical_parent.show_message('goodname2 %s' % good_name_2)
            #   idx_goodslot = [i for i in range(len(clipslots)) if clipslots[i].has_clip and bool(clipslots[i].clip.name == good_name_1 or clipslots[i].clip.name == good_name_2)][0]
            #   self.canonical_parent.show_message('idx goodslot %s' % idx_goodslot)
              # --- paste clip in right place ---
            #   self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/COPYCLIP %s ; %s/PASTECLIP 2' % (int(idx+1),int(idx_goodslot+1),int(idx+1)))
              for slot_idx in list(range(len(clipslots)))[5:]: #we use only clipslots below the 6th row
                    if clipslots[slot_idx].has_clip:
                          all_clip_names.append(clipslots[slot_idx].clip.name)
                          all_names_dico.update({(idx,slot_idx):clipslots[slot_idx].clip.name})
      #   idx_goodslotagain = [i for i in range(len(all_clip_names)) if all_clip_names[i] == good_name_1 or all_clip_names[i] == good_name_2][0]
        for position, name in all_names_dico.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
              if good_name_2 in name:
                    good_track_idx,good_slot_idx=position
        if args == '1':
              self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/COPYCLIP %s ; %s/PASTECLIP 2' % (int(good_track_idx+1),int(good_slot_idx+1),str_loopertracks_idx))
        elif args == '2':
              self.canonical_parent.show_message('args 2, goodtrack %s,goodslot %s ' % (good_track_idx,good_slot_idx))
              for idx in idx_loop_tracks:
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/COPYCLIP %s ; %s/PASTECLIP 2' % (int(idx+1),int(good_slot_idx+1),int(idx+1))) 
      #   self.canonical_parent.show_message('total beat asked %s' % total_beats_asked)
      #   self.canonical_parent.show_message('(all_clip_names) %s' % (all_clip_names))
      #   self.canonical_parent.show_message('goodnames %s,%s idx goodslotagain %s' % (good_name_1,good_name_2,idx_goodslotagain))
      #   self.canonical_parent.show_message('(dico) %s' % (all_names_dico))
      #   self.canonical_parent.show_message('goodtrack %s,goodslot %s ' % (good_track_idx,good_slot_idx))

     
      #   for i in range(len(idx_loop_tracks)):
      #         idx = idx_loop_tracks[i]
      #         track_loop = tracks[idx]
      #         clipslots = list(track_loop.clip_slots)
      #         for slot_idx in range(len(clipslots)):
      #               if slot.has_clip and slot.clip.name == all_clip_names[idx_goodslotagain]:
      #                     good_track_idx = idx
      #                     good_slot_idx = slot_idx
      #   self.canonical_parent.show_message('(goodtrack %s goodslot %s) ' % (good_track_idx,good_slot_idx))

      #   if good_track_idx != 0 and good_slot_idx != 0:
      #         self.canonical_parent.show_message('(goodtrack %s goodslot %s) ' % (good_track_idx,good_slot_idx))
              


             
    def adjust_length_loopclips(self, action_def, args):
        """like auto adjust binklooper but with multilooper config"""
        tracks, idx_bpm_ctrl_track, idx_cmdloop_tracks = [self.initialize_variables()[i] for i in (0,13,16)]
        init_clip_name = list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name
        list_bpm_arg=init_clip_name.split(' ')
        beat_arg=int(list_bpm_arg[-1])
        meas_arg=int(list_bpm_arg[-2])
        self.canonical_parent.show_message('idx cmdlooptracks %s' % idx_cmdloop_tracks)
        for i in range(len(idx_cmdloop_tracks)):
              idx = idx_cmdloop_tracks[i]
              track_cmd = tracks[idx]
              clip_cmd = list(track_cmd.clip_slots)[0].clip
              new_length = beat_arg*meas_arg
              #   new_length = 32
              #   clip_cmd.start_marker = 0
              self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/CLIP(1) LOOP START 0' % int(idx+1))
              self.canonical_parent.clyphx_pro_component.trigger_action_list('[] %s/CLIP(1) LOOP END %s' % (int(idx+1), new_length))
        self.canonical_parent.show_message('new meas/beat : %s/%s looplength : %s' % (meas_arg, beat_arg, float(beat_arg)*meas_arg))
      #   bpm_clip = list(tracks[0].clip_slots)[-4].clip
      #   init_bpm_name = bpm_clip.name
      #   name_splitted = init_bpm_name.split(' ')
      #   new_bpm_name = name_splitted[0] + ' ' + str(meas_arg) + ' ' + str(beat_arg)
      #   bpm_clip.name = new_bpm_name



    def switch_beatmidi(self, action_def, args):
        """all beats / fills / SC are loaded in big drmrcks. this function transposes midi notes to trigger new beat groups in the drum racks. beat base name can be specified in args"""
        tracks, names_beats_midi = [self.initialize_variables()[i] for i in (0,15)]
        idx_track_beatsmidi = [i for i in range(len(tracks)) if "beatsMidi" in tracks[i].name][0]
        track_beatsmidi = tracks[idx_track_beatsmidi]
        idx_track_fillsmidi = [i for i in range(len(tracks)) if "fillsMidi" in tracks[i].name][0]
        track_fillsmidi = tracks[idx_track_fillsmidi]
        idx_track_SCsmidi = [i for i in range(len(tracks)) if "SCMidi" in tracks[i].name][0]
        track_SCmidi = tracks[idx_track_SCsmidi]
        all_tracks_midi = [track_beatsmidi,track_fillsmidi,track_SCmidi]
        all_idx_midi=[idx_track_beatsmidi,idx_track_fillsmidi,idx_track_SCsmidi]
        self.canonical_parent.show_message('names beatsmidi : %s' % names_beats_midi)
         # --------------- find current beat base name ----------- AJOUTER TESTS ARGS
        beatsmidi_slots=list(track_beatsmidi.clip_slots)
        self.canonical_parent.show_message('beatsmidislot : %s ' % (beatsmidi_slots))
        currentbeat_slot = [beatsmidi_slots[i] for i in range(len(beatsmidi_slots)) if beatsmidi_slots[i].has_clip and "CurrentBeat" in beatsmidi_slots[i].clip.name][0] # "CurrentBeat" in beatsmidi_slots[i].clip.name]
        self.canonical_parent.show_message('currentbeatslot : %s ' % (currentbeat_slot))
        current_beat_name=currentbeat_slot.clip.name.split(' : ')[1]
        self.canonical_parent.show_message('current_beat_name : %s ' % (current_beat_name))
        idx_currentbeat = [i for i in range(len(names_beats_midi)) if current_beat_name in names_beats_midi[i]][0]
        idx_argsbeat = [i for i in range(len(names_beats_midi)) if args in names_beats_midi[i]][0]
        # ---------------- get samples names --------------
        for j in range(len(all_tracks_midi)):
              # --------------- find first occurence of base name in samples names -----------
              devices = list(all_tracks_midi[j].devices)
              self.canonical_parent.show_message('midi beat devices : %s ' % (devices))
              idx_drumrack = [z for z in range(len(devices)) if devices[z].can_have_drum_pads][0]
              idx_pitchdev = [z for z in range(len(devices)) if "Pitch" in devices[z].name][0]
              drmrck=devices[idx_drumrack]
              chains=list(drmrck.chains)
              self.canonical_parent.show_message(' drmrck chain device : %s ' % (list(chains[0].devices)[0]))
              # ----------- For Later : instead of increasing pitch by 4 all the time, might adapt to number of samples in each beat ---------
            #   chains_with_currentbeat=[]
            #   for i in range(len(chains)):
            #         if len(list(chains[i].devices)) > 0:
            #               simpler_dev = list(chains[i].devices)[0]
            #               if current_beat_name in chains[i].name: # For later : Try to stop loop as soon as other base beat names arrives ?
            #                     chains_with_currentbeat.append(chains[i])
            #         else:
            #               chains_with_currentbeat.append(chains[i]) # If no device on chain, still count it to increase the pitch of midi note
            #   self.canonical_parent.show_message('len chainswithcurrentbeat : %s ' % len(chains_with_currentbeat))
              # --------------- transpose midi notes according to first occurence position -------------
              param_pitch = devices[idx_pitchdev].parameters
              param_pitch_names=[param_pitch[z].name for z in range(len(param_pitch))]
              idx_param_pitch_pitch = [z for z in range(len(param_pitch)) if "Pitch" in param_pitch[z].name][0]
              if args and args in names_beats_midi:
                    param_pitch[idx_param_pitch_pitch].value += (idx_argsbeat-idx_currentbeat)*4
              else:
                    if idx_currentbeat < len(names_beats_midi)-1:
                        #   param_pitch[idx_param_pitch_pitch].value += len(chains_with_currentbeat) # Complex version
                          param_pitch[idx_param_pitch_pitch].value += 4
                    else:
                          param_pitch[idx_param_pitch_pitch].value = 0
              self.canonical_parent.show_message('param pitch %s' % param_pitch[idx_param_pitch_pitch].value)
        # --------------- Over write CurrentBeat name --------------
        if args and args in names_beats_midi:
                    currentbeat_slot.clip.name=currentbeat_slot.clip.name.split(' : ')[0] + ' : ' + names_beats_midi[idx_argsbeat]
        else:
              if idx_currentbeat < len(names_beats_midi)-1:
                    currentbeat_slot.clip.name=currentbeat_slot.clip.name.split(' : ')[0] + ' : ' + names_beats_midi[idx_currentbeat+1]
              else:
                    currentbeat_slot.clip.name=currentbeat_slot.clip.name.split(' : ')[0] + ' : ' + names_beats_midi[0]
        # --------- NEED ADJUST CLIP MIDI ACCORDING TO THE NOTE + PITCH ADDED

        # ------------- Tests -----------
        if not args :
              self.canonical_parent.show_message('no args' )
        elif args and args not in names_beats_midi:
              self.canonical_parent.show_message('args : %s not in names beats midi' % args )
        else:
              self.canonical_parent.show_message('args : %s' % args )
      #   self.canonical_parent.show_message('idx args : %s idx current : %s' % (idx_argsbeat,idx_currentbeat) )
      #   self.canonical_parent.show_message('idx current beat : %s ' % idx_currentbeat)
      #   self.canonical_parent.show_message('idxdrumrack : %s idxpitch : %s ' % (idx_drumrack, idx_pitchdev))
      #   self.canonical_parent.show_message('idx param pitch : %s ' % idx_param_pitch_pitch)



      
    def adjust_length_beatmidi(self, action_def, _):
        """sets length of midi clip according to length of corresponding sample in the beat drum rack and in the fill drum rack"""
        tracks, idx_beats_group, live_sample_frames = [self.initialize_variables()[i] for i in (0,12, 14)]
        idx_track_beatsmidi = [i for i in range(len(tracks)) if "beatsMidi" in tracks[i].name][0]
        track_beatsmidi = tracks[idx_track_beatsmidi]
        idx_track_fillsmidi = [i for i in range(len(tracks)) if "fillsMidi" in tracks[i].name][0]
        track_fillsmidi = tracks[idx_track_fillsmidi]
        idx_track_SCsmidi = [i for i in range(len(tracks)) if "SCMidi" in tracks[i].name][0]
        track_SCsmidi = tracks[idx_track_SCsmidi]
        all_tracks_midi = [track_beatsmidi,track_fillsmidi]
        all_idx_midi=[idx_track_beatsmidi,idx_track_fillsmidi]
        # Loop for each midi track
        for j in range(len(all_tracks_midi)):
      #   for j in range(1):
               # ------------ GET LENGTH for each sample -------------
              devices = list(all_tracks_midi[j].devices)
            #   self.canonical_parent.show_message('midi beat devices : %s ' % (devices))
              drmrck=devices[1] # first device is pitch, then comes rack
              chains=list(drmrck.chains)
              pitch=list(devices[0].parameters)[1].value
            #   self.canonical_parent.show_message('pitch param type %s' % (pitch) )
            #   self.canonical_parent.show_message(' drmrck chains : %s ' % (len(chains)))
              len_samples=[]
              cheat_lengths = [4,8,16,24,32,48,64] # CHEAT TO BE CHANGED
              namestest=[]
              iter_list = [z+int(pitch) for z in range(0,4)]# simple version : we work on 4 by 4 drum pads
            #   for i in range(len(chains)):
              for i in iter_list: # simple version : we work on 4 by 4 drum pads
                    raw_len = list(chains[i].devices)[0].sample.length # unit Frames
                    namestest.append(list(chains[i].devices)[0].name)
                    converted_len = raw_len / float(live_sample_frames)*float(self.song().tempo)/60 
                    # ======= BIG BIG CHEAT HERE ==========
                    converted_len = min(cheat_lengths, key=lambda x: abs(x-converted_len))
                  # ===================================
                    len_samples.append(converted_len)
            #   self.canonical_parent.show_message('raw len %s sampleframe %s tempo %s converted %s' % (raw_len,live_sample_frames,self.song().tempo, converted_len) )
            #   self.canonical_parent.show_message('converted %s' % (len_samples) )
              self.canonical_parent.show_message('chainnames %s' % (namestest) )

              # ------ ADD TEST WITH DEVICES[0].NAME IN CASE IT IS NOT A DRUMRACK DEVICE ------
              # ------------ SET LENGTH of each midi clip to corresponding sample ==== >> !!!!! CHEATED VERSION TO BE CHANGED !!!!!! << =======
              # ===================================
            #   cheat_lengths = [4,8,16,24,32,48,64]
            #   cheat_factor = 8/8.707507936507938
            #   len_samples=[len_samples[z]*cheat_factor for z in range(len(len_samples))]
            #   self.canonical_parent.show_message('kikou allidx= %s, j = %s, track = %s, len_samples %s ' % (all_idx_midi,j,all_tracks_midi[j].name,len_samples))
              # ===================================
              clipslots=list(all_tracks_midi[j].clip_slots)
              cliplengths=[]        
              for i in range(len(len_samples)):
                    
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) START 0' % (int(all_idx_midi[j]+1), int(i+1)))
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) LOOP START 0' % (int(all_idx_midi[j]+1), int(i+1)))
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) LOOP RESET' % (int(all_idx_midi[j]+1), int(i+1)))
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) LOOP END %s' % (int(all_idx_midi[j]+1), int(i+1),len_samples[i]))
                    # ---------- assumption : drum rack pads start at C1 = number 36 -----------
                    clipslots[i].clip.set_notes(((int(36+i),0,clipslots[i].clip.length,100,False),))
              self.canonical_parent.show_message('finito. len_samples %s ' % (len_samples))

               
            
                  

       
    def set_bpm_from_1bar_clip(self, action_def, _):
        """1 click : rec empty midi clip. 2nd click : stops rec, set bpm from midi clip length (1 bar)"""
        tracks, idx_bpm_ctrl_track = [self.initialize_variables()[i] for i in (0,13)]
        track_bpm = tracks[idx_bpm_ctrl_track]
        bpm_slots = list(track_bpm.clip_slots)
       # --------- find dummy slot and test if clip already existing or not ----------
        idx_cmd_1bar_slot=[i for i in range(len(bpm_slots)) if bpm_slots[i].has_clip and "bpm_1bar_clip" in bpm_slots[i].clip.name][0]
        idx_dummy_slot = idx_cmd_1bar_slot+1
        dummy_slot = bpm_slots[idx_dummy_slot] # the dummy slot to be created, measured and deleted is just under the command slot
        if dummy_slot.has_clip :
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/ARM OFF' % int(idx_bpm_ctrl_track+1) )
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP' % int(idx_bpm_ctrl_track+1) )
            # ------------------- get dummy clip length, delete dummy clip and set new bpm -------------------
            length_init = dummy_slot.clip.length # initial length based on corresponding measure length
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(%s) DEL' % (int(idx_bpm_ctrl_track+1), int(idx_dummy_slot+1)) )
            length_target = 4
            tempo_init = self.song().tempo
            tempo_target = tempo_init*length_target/length_init
            self.canonical_parent.show_message('ancient BPM %s new BPM %s' % (tempo_init, tempo_target))    
            self.canonical_parent.clyphx_pro_component.trigger_action_list('BPM %s' % tempo_target )
        else:
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/ARM ON' % int(idx_bpm_ctrl_track+1) )
            self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY %s' % (int(idx_bpm_ctrl_track+1),int(idx_dummy_slot+1)))
            



        

    def set_tinypad_configuration(self, action_def, arg):
        """as transport buttons are not supported for button binding in clyphx, this function changes the name of xclips with transport button functions depending on argument"""
        tracks=list(self.song().tracks)
        idx_tiny_transport_track = [i for i in range(len(tracks)) if "TinyTransports" in tracks[i].name ][0] # Carefull of not changing name of track
        tiny_transport_track=tracks[idx_tiny_transport_track]
        idx_tiny_notes_track=[i for i in range(len(tracks)) if "TinyNotes" in tracks[i].name ][0] # Carefull of not changing name of track
        tiny_notes_track=tracks[idx_tiny_notes_track]
        if arg == "0" :
            tiny_transport_track.clip_slots[0].clip.name="[] 1/CLIP(1) DEL"
            tiny_transport_track.clip_slots[1].clip.name='[] "Beats"/SEL'
            tiny_transport_track.clip_slots[2].clip.name="[] navigate_clips"
            tiny_transport_track.clip_slots[3].clip.name='[] (PSEQ) "Voix"/ARM ON ; "Voix"/ARM OFF'
            tiny_transport_track.clip_slots[4].clip.name='[] "piano"/SEL ; "piano"/plugin_preset_change'
            tiny_transport_track.clip_slots[5].clip.name="[] switch_armed_instru"
            # ----
            tiny_notes_track.clip_slots[0].clip.name="[] inc_bpm_from_loop_arg 1"
            tiny_notes_track.clip_slots[1].clip.name="[] dec_bpm_from_loop_arg 1"
            tiny_notes_track.clip_slots[2].clip.name="[] inc_bpm_from_loop_arg 2"
            tiny_notes_track.clip_slots[3].clip.name="[] dec_bpm_from_loop_arg 2"
            tiny_notes_track.clip_slots[4].clip.name="[] inc_binklooper_beats"
            tiny_notes_track.clip_slots[5].clip.name="[] dec_binklooper_beats"
            tiny_notes_track.clip_slots[6].clip.name='[] "piano"/PLAY 7'
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
    
    def switch_armed_instru(self, action_def, _):
        """arm the instrument track next to that already armed, disarms all other"""
        tracks, idx_instru_group, idx_instru_tracks = [self.initialize_variables()[i] for i in (0,7,8)]
        idx_armed_instru = [idx_instru_tracks[i] for i in range(len(idx_instru_tracks)) if tracks[idx_instru_tracks[i]].arm]
        self.canonical_parent.show_message('idx instru armed : %s' % idx_armed_instru) 
        # Disarm current armed instru track and arms the next instru track (or arms the 1st instru track if the current armed track is the last instru)
        tracks[idx_armed_instru[0]].arm = False
        if idx_armed_instru[0]+1 <= max(idx_instru_tracks) and tracks[idx_armed_instru[0]+1].name is not "voix": # TO BE CHANGED
              tracks[idx_armed_instru[0]+1].arm = True
        else:
              tracks[idx_instru_tracks[0]].arm = True


    def reset_instru_tracks(self, action_def, _):
        """deleted all tracks from INSTRU group excepted piano and bass track"""
        tracks, idx_instru_group, idx_instru_tracks = [self.initialize_variables()[i] for i in (0,7,8)]
        for i in range(len(idx_instru_tracks)-2):
              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/DEL' % int(idx_instru_tracks[-1-i]+1) )
        self.canonical_parent.clyphx_pro_component.trigger_action_list('"piano"/ARM ON')
        self.canonical_parent.clyphx_pro_component.trigger_action_list('"basse"/ARM ON')
      
   
    def play_rec_clip(self, action_def, _):
        """play top clip of rec. conditions on muting looper tracks depending on the state of routing"""
        self.canonical_parent.show_message('coucou00') 
        tracks, idx_loop_tracks, name_routing_clip = [self.initialize_variables()[i] for i in (0,1,6)]
        self.canonical_parent.show_message('name routing : %s' % name_routing_clip) 
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
        bpm_clip = [slot for slot in list(tracks[0].clip_slots) if slot.has_clip and "BPM" in slot.clip.name][0].clip
        init_bpm_name = bpm_clip.name
        name_splitted = init_bpm_name.split(' ')
        new_bpm_name = str(name_splitted[0]) + ' ' + str(meas_arg) + ' ' + str(time_arg)
        bpm_clip.name = new_bpm_name

    
    def increase_bpm_from_loop_arg(self, action_def, args):
        """ increases by 1 the beat numbers of bpm_from_loop argument or the measures number. if args = 1, measure number, if args = 2, beat numbers """ 
        tracks=list(self.song().tracks)
        idx_bpm_ctrl_track = [i for i in range(len(tracks)) if "bpm" in tracks[i].name][0] 
        self.canonical_parent.show_message('bpm track idx %s' % idx_bpm_ctrl_track )    
        init_clip_name = list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name
      #   base_name="[] SEL/bpm_from_loop_new " # MIGHT CHANGE IF BPM FROM LOOP FUNCTION CHANGES
        base_name=init_clip_name[0:-3]
        self.canonical_parent.show_message('base name %s' % base_name )               

        length_arg=len(init_clip_name)-len(base_name)
        str_bpm_arg = init_clip_name[-length_arg:]
        list_bpm_arg=str_bpm_arg.split(' ')
        meas_arg = int(list_bpm_arg[0])
        time_arg=int(list_bpm_arg[1])
      #   self.canonical_parent.show_message('coucou' )   
        if int(args) == 1: # modify measure numbers
              if meas_arg < 8:
                    meas_arg = meas_arg+1
              else:
                    meas_arg=8
              self.canonical_parent.show_message('new meas arg %s' % meas_arg) 
              list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name = base_name + str(meas_arg) + ' ' + list_bpm_arg[1]
        elif int(args) == 2: # modify beat numbers
              if time_arg < 9:
                    time_arg = time_arg+1
              else:
                    time_arg=9
              self.canonical_parent.show_message('new time arg %s' % time_arg) 
              list(tracks[idx_bpm_ctrl_track].clip_slots)[7].clip.name = base_name + list_bpm_arg[0] + ' ' + str(time_arg)
        else:
              self.canonical_parent.show_message('wrong argument, need 1 or 2' )   
        bpm_clip = [slot for slot in list(tracks[0].clip_slots) if slot.has_clip and "BPM" in slot.clip.name][0].clip
        init_bpm_name = bpm_clip.name
        name_splitted = init_bpm_name.split(' ')
        new_bpm_name = str(name_splitted[0]) + ' ' + str(meas_arg) + ' ' + str(time_arg)
        bpm_clip.name = new_bpm_name
    

    def delete_all_simpler_tracks(self, action_def, _):
        """ Deletes all Simpler tracks """
        tracks=list(self.song().tracks)
        string_music_track_names="Slice"
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


#     def increment_plugin_preset(self, action_def, args):
#         """increment plugin preset index in program list"""
#         track = action_def['track']   
#         track_idx = list(self.song().tracks).index(action_def['track']) 
#         self.canonical_parent.show_message('devices %s' % track.devices[0].chains[0].devices[0].name)
#         if track.devices[0].chains[0].devices[0].selected_preset_index >= 4:
#               track.devices[0].chains[0].devices[0].selected_preset_index = 0
#         else:
#               track.devices[0].chains[0].devices[0].selected_preset_index += 1 
    

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
        idx_track = list(self.song().tracks).index(action_def['track'])
        tracks, idx_instru_group, idx_instru_tracks, idx_sel_track_init= [self.initialize_variables()[i] for i in (0,7,8,10)]
        self.canonical_parent.show_message('pouet : ' ) 
        self.canonical_parent.show_message('idx instru tracks : %s' % idx_instru_tracks) 
        idx_last_instru = idx_instru_tracks[-1]
        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL ; %s/CLIP(1) TOSIMP ; WAIT 10 ; %s/SEL' % (int(idx_last_instru+1),int(idx_track+1), int(idx_sel_track_init+1)) )
      #   self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/set_simpler_slice 4' % int(idx_last_instru+2) )
      #   self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/SEL' % (int(idx_last_instru+1)),int(idx_track+1) )
   

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
        if len(idx_clipslots_full) > 0 :
             #  --------------  get current bpm and calculate target bpm -----------------
              if "REC" in sel_track.name:
                    length_init = list(sel_track.clip_slots)[0].clip.length
              length_target = float(args[0])*float(args[1])  
              tempo_init = self.song().tempo
            #   odd_measures = [3,5,6,7,9,10,11] #List of args that will take into account time sig change
            #   if length_target in odd_measures:
            #       #   time_sig_factor = 4/length_target # !!!!!!!! CA VA PAS CE FACTEUR !!!!!!!!!
            #         time_sig_factor = 1 
            #   else:
            #         time_sig_factor = 1              
              ratio_length_generic = length_target/length_init # can be used for all measure clips and for bpm
              tempo_target = tempo_init*ratio_length_generic
              self.canonical_parent.show_message('ancient length %s target length %s' % (length_init, length_target))    
            #   self.canonical_parent.show_message('ancient BPM %s new BPM %s' % (tempo_init, tempo_target))    
            #  --------------  Change bpm -----------------
              self.canonical_parent.clyphx_pro_component.trigger_action_list('BPM %s' % tempo_target ) 
              self.canonical_parent.clyphx_pro_component.trigger_action_list('1/CLIP(1) START 0 ; 1/CLIP(1) END %s' % length_target ) 
                 
        else:
            self.canonical_parent.show_message('No clip in Loop track or wrong track selected')
     

    def get_clip_length(self, action_def, _): 
        """ prints clip length """
        clip = action_def['clip']
        if clip: 
            self.canonical_parent.show_message('Clip length in beats : %s' % clip.length) 
            return clip.length
        else:
            self.canonical_parent.show_message('No clip object')


# ---------------------------------------------------------
   # ---------- End of Custom Functions -----------------
# ---------------------------------------------------------






    def global_action_example(self, action_def, args):
        """ Logs whether the action was triggered via an X-Clip and shows 'Hello World'
        preceded by any args in Live's status bar. """
        self.canonical_parent.log_message('X-Trigger is X-Clip=%s'
                                          % action_def['xtrigger_is_xclip'])
        self.canonical_parent.show_message('%s: Hello Worldddd' % args)

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
            else:
                self.canonical_parent.log_message('Error: Tried to rename X-Clip!')
