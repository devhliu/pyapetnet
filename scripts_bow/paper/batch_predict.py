import sys
import os
if not os.path.join('..','..') in sys.path: sys.path.append(os.path.join('..','..'))

import pickle
import h5py
import nibabel as nib
import numpy   as np

from glob             import glob
from pyapetnet.zoom3d import zoom3d
from keras.models     import load_model
from scipy.ndimage    import find_objects

#==========================================================================================
def load_nii(fname):
  nii = nib.load(fname)
  nii = nib.as_closest_canonical(nii)
  vol = nii.get_data()

  return vol, nii.affine

#==========================================================================================
def predict_from_nii(pet_input, 
                     mr_input, 
                     model_name, 
                     output_file, 
                     model_dir = os.path.join('..','..','data','trained_models'), 
                     perc = 99.99):

  # load the model
  with h5py.File(os.path.join(model_dir,model_name)) as model_data:
    training_voxsize = model_data['header/internal_voxsize'][:] 
  model            = load_model(os.path.join(model_dir,model_name))

  # read the input data
  mr_vol, mr_affine = load_nii(mr_input)
  mr_voxsize        = np.sqrt((mr_affine**2).sum(axis = 0))[:-1]
  bbox              = find_objects(mr_vol > 0.1*mr_vol.max(), max_label = 1)[0]
  mr_vol_crop       = mr_vol[bbox]
  crop_origin       = np.array([x.start for x in bbox] + [1])

  # update the affine after cropping
  mr_affine_crop         = mr_affine.copy()
  mr_affine_crop[:-1,-1] = (mr_affine_crop @ crop_origin)[:-1]

  # read the pet data
  pet_vol, pet_affine = load_nii(pet_input)
  pet_vol_crop        = pet_vol[bbox]

  # interpolate the volumes to the internal voxelsize of the trained model 
  zoomfacs            = mr_voxsize / training_voxsize
  mr_vol_crop_interp  = zoom3d(mr_vol_crop, zoomfacs)
  pet_vol_crop_interp = zoom3d(pet_vol_crop, zoomfacs)

  # normalize the input
  pmax = np.percentile(pet_vol_crop_interp, perc)
  mmax = np.percentile(mr_vol_crop_interp, perc)

  pet_vol_crop_interp /= pmax
  mr_vol_crop_interp  /= mmax

  # make the prediction
  x = [np.expand_dims(np.expand_dims(pet_vol_crop_interp,0),-1), np.expand_dims(np.expand_dims(mr_vol_crop_interp,0),-1)]
  pred = model.predict(x).squeeze() 

  # unnormalize the data
  pred                *= pmax
  pet_vol_crop_interp *= pmax
  mr_vol_crop_interp  *= mmax

  # generat the output affine transform
  output_affine = mr_affine_crop.copy()
  for i in range(3):  output_affine[i,:-1] /= zoomfacs

  # save the prediction
  nib.save(nib.Nifti1Image(pred, output_affine), output_file)

  print('wrote: ', output_file)

  # save the bbox and the zoomfacs
  pickle.dump({'bbox':bbox, 'zoomfacs':zoomfacs}, open(os.path.splitext(output_file)[0] + '_bbox.pkl','wb'))

  return pred

#==========================================================================================
#==========================================================================================
#==========================================================================================

model_name = sys.argv[1]
dataset    = sys.argv[2]
osem_sdir  = sys.argv[3]
osem_file  = sys.argv[4]

mr_file   = 'aligned_t1.nii'

if dataset == 'mmr-fdg':
  mdir      = '../../data/test_data/mMR/Tim-Patients'
  pdirs     = glob(os.path.join(mdir,'Tim-Patient-*'))
elif dataset == 'signa-pe2i':
  mdir      = '../../data/test_data/signa/signa-pe2i'
  pdirs     = glob(os.path.join(mdir,'ANON????'))
elif dataset == 'signa-fet':
  mdir      = '../../data/test_data/signa/signa-fet'
  pdirs     = glob(os.path.join(mdir,'ANON????'))
elif dataset == 'signa-fdg':
  mdir      = '../../data/test_data/signa/signa-fdg'
  pdirs     = glob(os.path.join(mdir,'?-?'))

for pdir in pdirs:
  print(pdir)

  output_dir = os.path.join(pdir,'predictions',osem_sdir)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  output_file = os.path.join(output_dir, '___'.join([os.path.splitext(model_name)[0],osem_file]))

  if not os.path.exists(output_file):
    pred = predict_from_nii(os.path.join(pdir,osem_sdir,osem_file),
                            os.path.join(pdir,mr_file),
                            model_name,
                            output_file)
  else:
    print(output_file,' already exists.')
 

