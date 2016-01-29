import numpy as np
import subprocess as sp
import trackpy as tp
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd
#from trackpy.utils import print_update

def print_update(message):
    "Print a message immediately; do not wait for current execution to finish."
    try:
        clear_output()
    except Exception:
        pass
    print(message)
    sys.stdout.flush()

class detector(object):
    '''A background referenced particle detector.  It calucaltes an average image, taken from the earlist
    a few frames of a video.  Each of video frame is then compared to this background image.  If a particle
    exsits on the background image already, it is then either a background feature or a particle have never
    moved, therefore labeled as a FALSE particle.  Those particles not detected on the background image is 
    labeled as TRUE particle.

    Image reading     : FFMEPG (pyAV has problems with non-standard frame rate videos as of 2015)
    particle detection: softmatter/trackpy

    '''
    
    
    def __init__(self, video_file, resolution='default', frame_rate='default', frames=-1, bufsize=10**9):
        '''video_file : name of the video_file
        resolution : automatically detected with 'default'.  Override possible with an (int, int) tuple
        frame_rate : automatically detected with 'default'.  Override possible with an int
        frames     : processing a subset of frames (not implemented)
        bufsize    : allocate enough RAM for in memeory processing
        '''
        #self.frame_rate = frame_rate
        #x_size, y_size = resolution
        
        _FFMPEG_BIN = "ffmpeg" # Change it in PC?
        _FFPROBE_BIN = 'ffprobe'
        #get the number of frames
        #ffprobe -select_streams v -show_frames "Time_15BUnexp_Rack_1.1.h264"
        p = sp.Popen([_FFPROBE_BIN,
                    '-select_streams', 'v', '-show_frames', video_file], 
                     stdout=sp.PIPE)
        out = p.stdout.read()
        if frames != -1:
            self.img_nFrame = out.count('coded_picture_number=') #number of frames
        else:
            self.img_nFrame = frames
        out = out.splitlines()
        if frame_rate == 'default':
            self.frame_rate = 1./float([item.split("=")[1] for item in out if 'pkt_duration_time' in item][0])
            self.frame_rate = int(self.frame_rate)
        if resolution == 'default':
            x_size = int([item.split("=")[1] for item in out if 'width' in item][0])
            y_size = int([item.split("=")[1]  for item in out if 'height' in item][0])
        else:
            x_size, y_size = resolution
        #get the image stack
        command = [_FFMPEG_BIN,
                    '-i', video_file,
                    '-f', 'image2pipe',
                    '-vf', 'fps=%s'%self.frame_rate,
                    '-pix_fmt', 'rgb24',
                    '-vcodec', 'rawvideo', '-an', '-']
        pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=bufsize)
        raw_image = pipe.stdout.read(y_size*x_size*3*self.img_nFrame)
        # transform the byte read into a numpy array
        image =  np.fromstring(raw_image, dtype='uint8')
        del pipe
        self.img_stack = image.reshape((self.img_nFrame, y_size, x_size, 3))
        self.img_dim   = (x_size, y_size)


    def plot_partest(self, pars, axes):
        '''Sort of a one thing does all method. For visual inspection of whether the parameters provided
        will give a good result.

        pars : parameters to be tested (such as the one fed from the GUI)
        axes : a matplotlib.axes instance

        Result:
        A plot constrast an earlier frame with a later frame. Particles are plotted with '+', with the 
        True dots further plotted with 'o'.
        '''
        x, y, h, w, fr1, fr2, bckgrf1, bckgrf2, thld, diameter, minmass, maxdia, addArgs = pars
        x_max = x+w
        y_max = y+h
        sub_imgstack = self.img_stack[range(bckgrf1, bckgrf2) + [fr1, fr2],
                                      y : y_max,
                                      x : x_max,
                                      :]
        sub_imgstack = (0.2989*sub_imgstack[:,:,:,0].astype(float)) +\
                       (0.5870*sub_imgstack[:,:,:,1].astype(float)) +\
                       (0.1140*sub_imgstack[:,:,:,2].astype(float))
        sub_bckgrd  = np.mean(sub_imgstack[:-2,:,:].astype(float), axis=0).astype(int)
        sub_cr_imgs = (255 - \
                        np.clip(sub_bckgrd.astype(float) - \
                                sub_imgstack[-2:,:,:].astype(float), 0, 255)).astype(int)
        for i in [-2, -1]:
            axes[i+2].imshow(sub_imgstack[i],
                             cmap=cm.Greys_r)
            _f_df = tp.locate(sub_imgstack[i], 
                              diameter = diameter, 
                              minmass = minmass,
                              maxsize  = maxdia,
                              **addArgs)
            if len(_f_df)>1:
                _f_df['ST_dsty'] = [self._area_density(_f_df.ix[j, 'x'], 
                                                       _f_df.ix[j, 'y'],
                                                       _f_df.ix[j, 'size'], 
                                                       255-sub_cr_imgs[i+2]) 
                                    for j in range(len(_f_df))]
                _f_df['True_particle'] = (_f_df['ST_dsty']>thld)
                axes[i+2].scatter(_f_df.ix[_f_df['True_particle'], 'x'],
                                  _f_df.ix[_f_df['True_particle'], 'y'],
                                  color='r',
                                  alpha=0.25,
                                  s=30)
                axes[i+2].scatter(_f_df.x,
                                  _f_df.y,
                                  marker='+',
                                  alpha=0.25,
                                  s=50)

        

    def show_ROI(self, x_lim, y_lim):
        '''display the region of interest (ROI). Using the 1st frame as reference image.
        '''
        x_min, x_max = x_lim
        y_min, y_max = y_lim
        #limit_high = 350
        #limit_low  = limit_high+240
        #limit_left = 485
        #limit_right= limit_left+320
        #show the first frame, part of it
        plt.imshow(self.img_stack[0,
                                  y_min : y_max,
                                  x_min : x_max,
                                  :])
        ax = plt.gca()
        xt = [item+x_min for item in ax.get_xticks().tolist()]
        yt = [item+y_min for item in ax.get_yticks().tolist()]
        ax.set_xticklabels(xt)
        ax.set_yticklabels(yt)

        
        
    def set_ROI(self, x_lim, y_lim):
        '''defines the region of interest (ROI) and convert the image into grayscale image
        '''
        x_min, x_max = x_lim
        y_min, y_max = y_lim
        #apply ROI to image stack
        self.img_stack = self.img_stack[:,
                                        y_min : y_max,
                                        x_min : x_max,
                                        :]
        #convert RGB to GrayScale
        self.img_stack = (0.2989*self.img_stack[:,:,:,0].astype(float)) +\
                         (0.5870*self.img_stack[:,:,:,1].astype(float)) +\
                         (0.1140*self.img_stack[:,:,:,2].astype(float))

                
                
    def show_30frames(self):
        '''Show the 1st 30 frames of a video, in a 5*6 subplot
        '''
        fig, axes = plt.subplots(nrows=5, ncols=6, figsize=(20, 14))
        for i, ax in enumerate(axes.ravel()):
            ax.imshow(self.img_stack[i,:,:], cmap=cm.Greys_r)
            ax.axis('off')
            ax.set_title('Frame No. %s'%(i+1))

            
            
    def set_backgrd(self, frames, how='mean'):
        '''calculate the mean, or the median (controlled by `how`) of the set of image defined by `frames`
        and use the resultant as the background image. 
        '''
        if how == 'mean':
            f  = np.mean
        if how == 'median':
            f  = np.median
        if len(frames)==2:
            frame_start, frame_end = frames
            #TODO: add an exception (remind user to set_ROI first)
            #if len(self.img_stack) == 4:
            #    pass
        
            #background, calulated from first a few frames
            self.bkgrd_image = f(self.img_stack[frame_start:frame_end,:,:].astype(float), 
                                 axis=0).astype(int)
        else:
            self.bkgrd_image = f(self.img_stack[frames,:,:].astype(float),
                                 axis=0).astype(int)
        #corrected image, calulated from background substraction
        self.crtd_image = (255 - \
                           np.clip(self.bkgrd_image.astype(float) - \
                                   self.img_stack.astype(float), 0, 255)).astype(int)

        
    def _area_density(self, x, y, r, img):
        '''return the density of the cicle, with radius `r`, centered at `(x, y)`, on image `img`'''
        #x, y coordinates
        y_arr, x_arr = np.indices(img.shape)
        mask         = (((x_arr-x)**2 + (y_arr-y)**2) < r*r)
        #plt.imshow(mask)
        return (img.astype(float)*mask).sum()



    def bckgrd_pdetect(self, thld=100, progress_barF=None, Print=True, **kwargs):
        '''Such as:
        P_dfs = bckgrd_pdetect(thld=125,
                      diameter=(5,5), 
                      minmass=300, 
                      invert=True)
        thld : thershold, a TRUE particle must be darker than the backgroud image by this amount
        progress_barF : a handle for external status bar (such as in a GUI)
        Print         : print out this frame number that is currently processing
        **kwars       : additional parameters passed to trackpy.locate() method

        Returns
        a pandas.DataFrame containing the information of all particles (both True and False ones) detected
        '''
        particle_dfs = []
        for _idx, _img in enumerate(self.img_stack):
            if progress_barF is None:
                pass
            else:
                progress_barF(_idx, len(self.img_stack))
            _f_df = tp.locate(_img, **kwargs)
            if len(_f_df)>1:
                _f_df['ST_dsty'] = [self._area_density(_f_df.ix[i, 'x'], 
                                                       _f_df.ix[i, 'y'],
                                                       _f_df.ix[i, 'size'], 
                                                       255-self.crtd_image[_idx]) 
                                    for i in range(len(_f_df))]
                _f_df['True_particle'] = (_f_df['ST_dsty']>thld)
                _f_df['Timestamp']     = _idx*(1./self.frame_rate) #if frame rate is know may convert to timestamp
                _f_df['frame']         = _idx                      #must have it to make the tracker work
            particle_dfs.append(_f_df)
            if Print:
                print_update('Analyzing frame %s'%_idx)
            self.particle_dfs = particle_dfs
        return particle_dfs



    def diagnostic_plot(self, img_index, ax=None, SZ_true_dot=30, SZ_fake_dot=50):
        '''Diagnostic plot of tracking result
        
        img_index  : which frame to be plotted.
        ax         : a matplotlib.axes, will create a new one if not provided
        SZ_true_dot: marker size for true particles
        SZ_fake_dot: marker size for fake particles

        returns the matplotlib.axes instance.
        In the plot, the dots are plotted as '+' and the true dots are further superimposed with 'o'
        '''
        f_df = self.particle_dfs[img_index]
        #actually plotting
        if ax==None:
            fig = plt.figure()
            ax  = plt.gca()
        ax.imshow(self.img_stack[img_index],
                  cmap=cm.Greys_r)
        ax.scatter(f_df.ix[f_df['True_particle'], 'x'],
                   f_df.ix[f_df['True_particle'], 'y'],
                   color='r',
                   alpha=0.25,
                   s=SZ_true_dot)
        ax.scatter(f_df.x,
                   f_df.y,
                   marker='+',
                   alpha=0.25,
                   s=SZ_fake_dot)
        return ax
    


    def particle_tracking(self, search_range, length_cutoff, **kwargs):
        '''Tracking method. One must run particle detection first before this. 
        
        search_range : the max distance that two particles will be joined in one track
        length_cutoff: the min length (in frames) that a track must have
        **kwargs     : other parameters passed to trackpy.link_df method

        returns: pandas.DataFrame containing the tracks
        '''
        #must use a dataframe containing true dots only
        particles = pd.concat([item[item.True_particle] for item in self.particle_dfs])
        tracks    = tp.link_df(particles, search_range=search_range, **kwargs)
        if length_cutoff > 0:
            tracks = tp.filter_stubs(tracks, length_cutoff)
        self.tracks = tracks
        return tracks
