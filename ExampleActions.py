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
        self.add_clip_action('get_clip_length', self.get_clip_length)
        self.add_clip_action('fill_with_do', self.add_note_to_empty_midi_clip)
        self.add_clip_action('audio_to_simp', self.send_audio_clip_to_simpler)
        self.add_clip_action('bpm_from_loop', self.set_new_bpm_from_loop_length)
        self.add_track_action('set_simpler_free', self.set_simpler_track_free_performance)
        self.add_track_action('switch_loop_source', self.switch_play_from_audiotrack_to_simplertrack)
        self.add_track_action('get_track_index', self.get_track_index)
        self.add_global_action('get_track_number', self.get_track_number)
        self.add_global_action('count_playing_clips', self.count_playing_clips)
        self.add_track_action('play_from_last', self.play_counting_from_last_clip)
        self.add_track_action('set_simpler_slice', self.set_simpler_slice)
        self.add_track_action('plugin_preset_change', self.increment_plugin_preset)
        self.add_global_action('set_binklooper_beats', self.set_binklooper_beats)
        self.add_global_action('inc_binklooper_beats', self.increase_binklooper_beats)
        self.add_global_action('dec_binklooper_beats', self.decrease_binklooper_beats)
        self.add_global_action('simplers_to_rec', self.simplers_clips_to_rec_clip)
      #   self.add_track_action('set_simpler_loop_on', self.set_simpler_loop_on)
      #   self.add_clip_action('send_clip_to_simpler', self.send_audio_clip_to_existing_simpler)
#  didnt find function to replace simpler sample 
#     def send_audio_clip_to_existing_simpler(self, action_def, args):
#         """ like TOSIMP but sending to existing simpler track """
#         clip = action_def['clip']
#         if clip:
#               nb_simpler = args


#         else:
#               self.canonical_parent.show_message('no clip object') 


    def simplers_clips_to_rec_clip(self, action_def, _):
        """ sends all simpler playing clips to an audio rec clip on 1st REC track. if pressed again, launches the rec clip """
        all_tracks=list(self.song().tracks)
        track_rec=all_tracks[0]
        index_simplers = [i for i in range(len(all_tracks)) if "Simpler" in all_tracks[i].name]
        rec_clipslots=list(track_rec.clip_slots)
        rec_clipslots_empty = [i for i in range(len(rec_clipslots)) if not rec_clipslots[i].has_clip]
      #   CONDITION : we want to play press to the rec clip whether it is already recording (existing) or not existing yet 
        index_first_empty_slot = rec_clipslots_empty[0]
        self.canonical_parent.show_message('target slot : %s, new clip : %s' % (index_first_empty_slot+1, not rec_clipslots[index_first_empty_slot-1].is_playing) )
        if not rec_clipslots[index_first_empty_slot-1].is_playing:
              for i in range(len(index_simplers)):
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/OUT "%s"' % (int(index_simplers[i]+1), all_tracks[0].name)) 
            # create new clip 
              self.canonical_parent.clyphx_pro_component.trigger_action_list('1/PLAY %s' % int(index_first_empty_slot+1)) 
        else:
            # launch the previously created clip
              self.canonical_parent.clyphx_pro_component.trigger_action_list('1/PLAY %s' % index_first_empty_slot) 
            #  stop simpler tracks so that only the rec track remains, reset simplers outputs to Master
              for i in range(len(index_simplers)):
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP' % int(index_simplers[i]+1))
                    self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/OUT "Master"' % int(index_simplers[i]+1))      

    def decrease_binklooper_beats(self, action_def, _):
        """ decreases by 1 the beat numbers of binklooper in 1st track, changes its name to display new beat nb """
        track_bink=list(self.song().tracks)[0]
        param_bink=list(track_bink.devices)[0].parameters
        self.canonical_parent.show_message('beats %s' % type(param_bink[5].value)) #param[5] is loop length
        param_bink[5].value -= 1
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
        if track.devices[0].selected_preset_index >= 4:
              track.devices[0].selected_preset_index = 0
        else:
              track.devices[0].selected_preset_index += 1 
    
    def set_simpler_slice(self, action_def, args):
        """set simpler in slice mode right after being created, split into 1 beat clip"""
        track = action_def['track']   
        track_idx = list(self.song().tracks).index(action_def['track']) 
        self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/ARM ON ; SEL/INSUB "Ch. 16"')
        self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/DEV(1) SIMP PLAYMODE 3 ; SEL/DEV(1) SIMP WARP ON ; SEL/DEV(1) SIMP GATE OFF') #mode 3 = slice
        simpler=track.devices[0]
        simpler.sample.slicing_style = 1 # slice by beat
        simpler.sample.slicing_beat_division = int(args) # test
        simpler.sample.gain = 0.6 # => 8 db
      
        
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
                    
    def switch_play_from_audiotrack_to_simplertrack(self, action_def, _):
        """ stops audio clip from audio track and launches clip in simpler track """
        track = action_def['track'] 
        if track:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('1/STOP')
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/PLAY 1')
              self.canonical_parent.show_message('sample : %s' % action_def)
        else:
              self.canonical_parent.show_message('No track object')


#     def set_simpler_loop_on(self, action_def, _):
#         """ Right after creating simple track : resize midi simpler clip length, 
#         changes track name to SIMPLER X, sets playmode to classic, sets utility gain to match initial loop,
#          sets track color and adds a midi clip filled with C3 for the simpler to be ready to play"""
#         track = action_def['track']   
#         self.canonical_parent.show_message('%s' % list(track.devices)[0].playback_mode)
#       #   retrig = list(track.devices)[0].sample.retrigger
        
        


    def set_simpler_track_free_performance(self, action_def, _):
        """ Right after creating simple track : resize midi simpler clip length, 
        changes track name to SIMPLER X, sets playmode to classic, sets utility gain to match initial loop,
         sets track color and adds a midi clip filled with C3 for the simpler to be ready to play"""
        track = action_def['track']   
        initial_nb_tracks = 5 # VERY IMPORTANT PARAMETER
        actual_nb_tracks = len(list(self.song().tracks))
        new_simpler_index = actual_nb_tracks - initial_nb_tracks
      #   track_index = list(self.song().tracks).index(action_def['track']) # ! track index starts at 0
        track_color = 1+(new_simpler_index-1)*5 #doesnt work, new track always at same place !
        # ------------------ Make sample length conversion from sample frames unit to beats unit ------------------
        # ------------------ This will be used to set the simpler clip note length  ------------------
        sampling_freq = 44100 # VERY IMPORTANT PARAMETER - Frequence dechantillonage en FR
        conversion_factor_sample = self.song().tempo/60/sampling_freq
        sample_length_frame_unit = list(track.devices)[0].sample.end_marker
        sample_length_beat_unit = sample_length_frame_unit*conversion_factor_sample
        sample_length_bar_unit = sample_length_beat_unit/4
        if track:
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/NAME "Simpler %s"' % new_simpler_index)
              sample_length_frame_unit = list(track.devices)[0].playback_mode = 0
            #   self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/DEV SIMP PLAYMODE CLASSIC')
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/Color %s' % track_color)
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/ADDCLIP 1 %.3f' % sample_length_bar_unit)
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/user_clip(1) fill_with_do')
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/DEV("Utility") "Gain" 80') #sets gain to 9 dB
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/DEV("BINK looper") DEL')
              self.canonical_parent.show_message('%.7f' % sample_length_bar_unit) 
        else:
              self.canonical_parent.show_message('No track object')


    def set_new_bpm_from_loop_length(self, action_def, args):
        """ sends audio clip to simpler """
        clip = action_def['clip']   
        self.canonical_parent.show_message('ya qqun %s' % args)
        if clip:
             #  --------------  get current bpm and calculate target bpm -----------------
              length_init = clip.length
              length_target = float(args)  
              tempo_init = self.song().tempo
              odd_measures = [3,5,6,7,9,10,11] #List of args that will take into account time sig change
              if length_target in odd_measures:
                    time_sig_factor = 4/length_target
              else:
                    time_sig_factor = 1              
              tempo_target = tempo_init*length_target/length_init*time_sig_factor
              time_sig_target = int(args)
              self.canonical_parent.show_message('ancient BPM %s new BPM %s' % (tempo_init, tempo_target)) 
              self.canonical_parent.clyphx_pro_component.trigger_action_list('BPM %s' % tempo_target )
              ratio_length_generic = length_target/length_init*time_sig_factor # can be used for all simplers
              # -------------------- prepare loop for all simplers ---------------
              initial_nb_tracks = 5 # VERY IMPORTANT PARAMETER
              actual_nb_tracks = len(list(self.song().tracks))
              nb_of_simplers_present = actual_nb_tracks - initial_nb_tracks
              for i in range(1,nb_of_simplers_present+1):
                    cliplength_init = list(self.song().tracks)[i].clip_slots[0].clip.length
                    cliplength_target = cliplength_init*ratio_length_generic
                    idx_track = int(i+1)
                    self.canonical_parent.show_message('Last TR: %s, last length: %s' % (i+1,cliplength_target)) 
                    isplaying = list(self.song().tracks)[i].clip_slots[0].clip.is_playing
                    if isplaying:
                        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP ; %s/CLIP(1) LOOP END %.2f' % (idx_track,idx_track,cliplength_target)) 
                        if tempo_init < tempo_target:
                              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(1) NOTES EXP' % idx_track)  
                        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/PLAY 1' % idx_track)
                    else:
                        self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/STOP ; %s/CLIP(1) LOOP END %.2f' % (idx_track,idx_track,cliplength_target)) 
                        if tempo_init < tempo_target:
                              self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/CLIP(1) NOTES EXP' % idx_track)  
        else:
            self.canonical_parent.show_message('No clip object')
        


    def send_audio_clip_to_simpler(self, action_def, args):
        """ sends audio clip to simpler """
        clip = action_def['clip']   
        self.canonical_parent.show_message('ya qqun %s' % args)
        if clip:
              # ------- send clip to simpler with a 12 dB utility device
              self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/CLIP(SEL) TOSIMP')
        else:
            self.canonical_parent.show_message('No clip object')
              


    def add_note_to_empty_midi_clip(self, action_def, _):
        """ sets new bpm from ratio between actual clip length and desired length"""
        clip = action_def['clip']   
        if clip:
              clip.set_notes(((60,0,clip.length,100,False),))
              self.canonical_parent.show_message("C3 added to %s" % clip.name )
        else:
             self.canonical_parent.show_message('No clip object')  

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

      
