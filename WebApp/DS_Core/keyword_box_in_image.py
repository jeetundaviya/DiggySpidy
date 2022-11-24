from importlib.resources import path
import easyocr as e_ocr
import cv2
import os

class KeywordBox:

	def get_keyword_ocr_result(self,keyword,image,all_matches=False):
		
		reader = e_ocr.Reader(['en'])

		keyword = keyword.lower()
		
		results = reader.readtext(image)
		
		if not all_matches:		

			for result in results:

				ocr_result = result[1].lower()

				if keyword in ocr_result:
					return result
		else:

			ocr_results = []

			for result in results:

				ocr_result = result[1].lower()

				if keyword in ocr_result:
					ocr_results.append(result)
					
			if len(ocr_results) > 0:
				return ocr_results

		return False


	def draw_box(self,ocr_result):


		top_left = (int(ocr_result[0][0][0]),int(ocr_result[0][0][1]))

		bottom_right = (int(ocr_result[0][2][0]),int(ocr_result[0][2][1]))

		text = ocr_result[1]

		# print(f'[+] {ocr_result}')

		font = cv2.FONT_HERSHEY_SIMPLEX

		img = cv2.imread(self.output_img)

		img= cv2.rectangle(img,top_left,bottom_right,(0,0,255),3)

		# img = cv2.putText(img,text,top_left,font,.5,(255,255,255),2,cv2.LINE_AA)

		cv2.imwrite(self.output_img,img)


	def __init__(self,input_image_folder,input_image,keyword,all_matches=False):
		self.image_name= input_image
		self.image_folder = input_image_folder
		self.image = os.path.join(input_image_folder,input_image) 
		input_img = cv2.imread(self.image)
		self.keyword = keyword
		self.all_matches = all_matches
		
		self.output_img = self.image

		cv2.imwrite(self.output_img,input_img)

		if all_matches:

			self.img_ocr_results = self.get_keyword_ocr_result(keyword=self.keyword,image=self.image,all_matches=True)

			if self.img_ocr_results:
				for ocr_result in self.img_ocr_results:
					self.draw_box(ocr_result)
				os.rename(self.output_img,os.path.join(self.image_folder,f'(FOUND){self.image_name}') )
			else:
				os.rename(self.output_img,os.path.join(self.image_folder,f'(NOT FOUND){self.image_name}') )
				# os.remove(self.output_img)
		else:
			
			self.img_ocr_result = get_keyword_ocr_result(keyword=self.keyword,image=self.image)

			if self.img_ocr_result:
				self.draw_box(ocr_result)
				os.rename(self.output_img,os.path.join(self.image_folder,f'(FOUND){self.image_name}') )
			else:
				os.rename(self.output_img,os.path.join(self.image_folder,f'(NOT FOUND){self.image_name}') )
				# os.remove(self.output_img)