"""
This file will allow the user to modify the generated image by performing some basic edits: smile, pose
Use the facial_editing directory to do the work.
"""
import numpy as np
# import sys

# sys.path.append("..")

# from encoder.InterFaceGAN.models.stylegan_generator import StyleGANGenerator
# from encoder.InterFaceGAN.utils.manipulator import linear_interpolate
# from ..facial_editing.utils.manipulator import project_boundary

AGE_BOUNDARY_PATH = "../encoder/InterFaceGAN/boundaries/stylegan_celebahq_age_w_boundary.npy" 
POSE_BOUNDARY_PATH = "../encoder/InterFaceGAN/boundaries/stylegan_celebahq_pose_w_boundary.npy" 
GENDER_BOUNDARY_PATH = "../encoder/InterFaceGAN/boundaries/stylegan_celebahq_gender_w_boundary.npy" 
SMILE_BOUNDARY_PATH = "../encoder/InterFaceGAN/boundaries/stylegan_celebahq_smile_w_boundary.npy" 

# have different sets of boundaries for now

# this is the class that we can import in the app.py file that does facial editing
class FaceModifier: # NOT TO BE INSTANTIATED ==> MORE LIKE AN INTERFACE REALLY
    def __init__(self):
        # self.model = StyleGANGenerator("stylegan_celebahq", None)
        # self.latent_space_type = "wp" # w+ latent space
        # self.kwargs = {'latent_space_type': self.latent_space_type}
        # # the 4 attribute bondaries 
        # self.age_boundary = np.load(AGE_BOUNDARY_PATH)
        # self.pose_boundary = np.load(POSE_BOUNDARY_PATH)
        # self.gender_boundary = np.load(GENDER_BOUNDARY_PATH)
        # self.smile_boundary = np.load(SMILE_BOUNDARY_PATH)
        self.latent_code = np.empty((1,18,512))

    def set_latent_code(self, latent_code):
        self.latent_code = latent_code

    # all the methods below conduct inferencing   
    def modify_latent_code(self, boundary, offset):
        # code=linear_interpolate(self.latent_code, 
        #                         boundary,
        #                         start_distance=offset,
        #                         end_distance=offset,
        #                         steps=1)

        # print(code.shape)
        # print("============================================================")
        # print("modified latent code is of shape:")
        # print(code.shape)
        # print("============================================================")

        # adding a multiple of the hyperplane before returning it
        modified_code = np.add(self.latent_code, np.multiply(boundary, offset))
        return modified_code

    def synthesize(self):
        outputs = self.model.easy_synthesize(self.latent_code, **self.kwargs) 
        return outputs['image']
    
    # each method only returns 1 image  --> offset = start_distance = end_distance
    def change_age(self, offset):
        self.latent_code = self.modify_latent_code(self.age_boundary, offset)

    def change_pose(self, offset):
        self.latent_code = self.modify_latent_code(self.pose_boundary, offset)
    
    def change_smile(self, offset):
        self.latent_code = self.modify_latent_code(self.smile_boundary, offset)

    def change_gender(self, offset):
        self.latent_code = self.modify_latent_code(self.gender_boundary, offset)
    
    def modify(self, age_offset,  gender_offset, pose_offset, smile_offset):
        # preprocessing
        # self.latent_code = self.model.preprocess(self.latent_code, **self.kwargs)
        
        # no modifications made to the image
        if (age_offset == 0) and (pose_offset == 0) and (smile_offset == 0) and (gender_offset == 0):
            return self.synthesize(), self.latent_code

        if age_offset != 0:
            self.change_age(age_offset)
        if pose_offset != 0:
            self.change_pose(pose_offset)
        if smile_offset != 0:
            self.change_pose(smile_offset)
        if gender_offset != 0:
            self.change_gender(gender_offset)

        output = self.synthesize()
        # print(output.shape)
        # print("=======================================") 
        # print(self.latent_code.shape)
        return output[0], self.latent_code
    
##########################################################################

# from dualstylegan import Model
from torch import from_numpy, clamp
# from PIL import Image

AGE_BOUNDARY_PATH_2 = "/home/sai_k/DualStyleGAN/hyperplanes/age.npy"
POSE_BOUNDARY_PATH_2 = "/home/sai_k/DualStyleGAN/hyperplanes/yaw.npy"
GENDER_BOUNDARY_PATH_2 = "/home/sai_k/DualStyleGAN/hyperplanes/gender.npy"
SMILE_BOUNDARY_PATH_2 = "/home/sai_k/DualStyleGAN/hyperplanes/mouth_open.npy"

class FaceModifier2(FaceModifier): # inherting from Facemodifier
    def __init__(self, model, device):
        super().__init__()
        # Inferencing on a GPU
        # self.device = device("cuda")
        # self.model = Model(device=self.device)
        self.model = model
        self.device = device
        # remember to unsqueeze them before adding to the latent code
        self.age_boundary = np.expand_dims(np.load(AGE_BOUNDARY_PATH_2,allow_pickle=True), axis=0)
        self.pose_boundary = np.expand_dims(np.load(POSE_BOUNDARY_PATH_2,allow_pickle=True), axis=0)
        self.gender_boundary = np.expand_dims(np.load(GENDER_BOUNDARY_PATH_2,allow_pickle=True), axis=0)
        self.smile_boundary = np.expand_dims(np.load(SMILE_BOUNDARY_PATH_2,allow_pickle=True), axis=0)

    def synthesize(self):
        codes2 = from_numpy(self.latent_code).to(self.device)
        # this bit is the decoder
        # NOTE: both of the returned items are pytorch tensors
        # NOTE: ignore the result_latent code -> it's utter garbage, just encodes a different face completely.
        img_rec, result_latent = self.model.encoder.decoder(
            [codes2],
            input_is_latent=False,
            randomize_noise=False,
            return_latents=True,
            z_plus_latent=True
        )

        img_rec = clamp(img_rec.detach(), -1, 1)
        img_rec = self.model.postprocess(img_rec[0])
        return img_rec


# need to import the latent code
# codes = np.load("/home/sai_k/DualStyleGAN/gui/randomface.npy", allow_pickle=True)
# boundary = np.load("/home/sai_k/DualStyleGAN/stylegan2directions/gender.npy", allow_pickle=True)
# boundary1 = np.expand_dims(boundary, axis=0)

# boundary2 = np.multiply(boundary1, -8)


# codes -= boundary2
# codes2 = from_numpy(codes)

# print("The dimensions of the generated image", end=":")
# print(img_rec.shape)

# Converting the numpy array into image
# img  = Image.fromarray(img_rec)
# print(type(img))
# Saving the image
# img.save(f"/home/sai_k/DualStyleGAN/gui/gender/modified_man_3.jpg")

# print("Images saved successfully")


# NOTE: we don't save the result_latent code cos it's utter garbage, just encodes a different face completely.
# np.save("./new_result_latent_2", result_latent.detach().numpy())
# arr = np.load("/home/sai_k/DualStyleGAN/gui/reconstructed_face.npy", allow_pickle=True)