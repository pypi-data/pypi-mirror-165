import os
from math import ceil

class AnnotationDataLoader:
	def __init__(self, labels, dataset_dir):
		self.labels = labels
		self.starting_num_images = len(os.listdir(os.path.join(dataset_dir, 'train' , 'images'))) + len(os.listdir(os.path.join(dataset_dir, 'valid' , 'images'))) 
		self.current_num_images = self.starting_num_images #TODO: update methods to actively track the current_num_images
		self.batch_ptr = 0
		self.input_dir = dataset_dir

		val_images, val_labels = self.get_train_val_data(self.input_dir)
		self.img_batches , self.label_batches, self.batch_type = self.batch_images(val_images, val_labels, starting_img_per_batch = 50)


	def update_number_images_taken(self, num_images_taken, absolute = False):
		if not absolute:
			self.current_num_images += num_images_taken
		else:
			self.current_num_images = num_images_taken

	def get_total_ds_imgs(self):
		return self.current_num_images
	
	def get_total_ds_imgs_added(self):
		return self.get_total_ds_imgs() - self.starting_num_images

	def has_next_batch(self):
		return len(self.img_batches) > 0 and self.batch_ptr < len(self.img_batches) 

	def get_next_batch_type(self):
		if not self.has_next_batch():
			raise Exception("Trying to access a batch that doesn't exist. The current len of self.img_batches is 0.")

		return self.batch_type[self.batch_ptr]

	def get_next_batch(self):
		if not self.has_next_batch():
			raise Exception("Trying to access a batch that doesn't exist. The current len of self.img_batches is 0.")

		self.batch_ptr += 1
		return (self.img_batches[self.batch_ptr - 1], self.label_batches[self.batch_ptr - 1])
	
	def reset_batch_ptr(self):
		self.batch_ptr = 0

	def clear_batches(self):
		self.img_batches.clear()
		self.label_batches.clear()
		self.reset_batch_ptr()

	def reset_and_update_batch_queue(self, img_batches, label_batches, batch_types):
		self.clear_batches()

		self.img_batches = img_batches
		self.label_batches = label_batches
		self.batch_type = batch_types

	def set_data_and_batch_evenly(self, images, labels, batch_type = 'val' ):

		if len(images) != len(labels):
			raise Exception(f'There must be an equal number of images and labels, currently we have {len(images)} images and {len(labels)} labels')

		img_batches = []
		label_batches = []
		batch_types = []
		
		imgs_per_batch = 256
		num_batches = ceil(len(images) / imgs_per_batch)
		lst_index = 0

		for j in range(num_batches):
			img_batches.append(images[lst_index : min(lst_index + imgs_per_batch, len(images))])
			label_batches.append( labels[lst_index : min(lst_index + imgs_per_batch, len(images))]                )
			batch_types.append(batch_type)
			lst_index += imgs_per_batch

			print(f'Batch {len(img_batches)} complete.')
			print(f'Batch size: {len(img_batches[-1])}')
		
		return img_batches , label_batches , batch_types

	def get_train_val_data(self, input_dir):

		val_images = []
		val_labels = []
		for trainval in ['train', 'valid']:
			
			for fname in os.listdir(os.path.abspath(os.path.join(input_dir, trainval, 'images'))):
				tail = os.path.split(fname)[-1]
				tail = tail[:tail.rfind('.')] #Get filename 
				if not (f'{tail}.txt' in os.listdir(os.path.join(input_dir, trainval, 'labels'))):
					val_images.append(os.path.abspath(os.path.join(input_dir, trainval, 'images', fname)))
					val_labels.append(os.path.abspath(os.path.join(input_dir, trainval, 'labels', f'{tail}.txt')))
		return val_images, val_labels

	def batch_images(self, val_images, val_labels,  starting_img_per_batch = 50):
		img_batches = []
		label_batches = []
		batch_type = []

		last_idx = 0
		val_imgs_per_batch = starting_img_per_batch
		for i in range(len(val_images)):
			image_batch = val_images[last_idx : min(len(val_images), last_idx + val_imgs_per_batch)]
			label_batch = val_labels[last_idx : min(len(val_images), last_idx + val_imgs_per_batch)]

			if last_idx + val_imgs_per_batch >= len(val_images):
				break

			last_idx = min(len(val_images), last_idx + val_imgs_per_batch)
			val_imgs_per_batch = min(val_imgs_per_batch * 2, 256)#

			img_batches.append(image_batch)
			label_batches.append(label_batch)
			batch_type.append('val')

		return img_batches, label_batches, batch_type