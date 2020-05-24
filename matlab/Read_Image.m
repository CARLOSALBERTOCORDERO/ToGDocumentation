Image=imread("IMAGE.tif");             % --Reading Image Data
B1=single(Image(:,:,1));               % --Reading Band 1
B2=single(Image(:,:,2));               % --Reading Band 2
B3=single(Image(:,:,3));               % --Reading Band 3
figure; 
subplot(2,2,1); imshow(Image); title('TIFF Image');
subplot(2,2,2); imshow(uint8(B1)); title('Band 1');
subplot(2,2,3); imshow(uint8(B2)); title('Band 2');
subplot(2,2,4); imshow(uint8(B3)); title('Band 3');