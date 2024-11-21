import { Asset } from 'react-native-image-picker';
import { Platform } from 'react-native';

interface ImageUpload {
  uri: string;
  type: string;
  name: string;
}

interface UploadResponse {
  success: boolean;
  url?: string;
  error?: string;
}

export const uploadImage = async (asset: Asset): Promise<UploadResponse> => {
  try {
    const imageData: ImageUpload = {
      uri: Platform.OS === 'ios' ? asset.uri!.replace('file://', '') : asset.uri!,
      type: asset.type || 'image/jpeg',
      name: asset.fileName || 'image.jpg',
    };

    const formData = new FormData();
    formData.append('image', imageData as unknown as Blob);

    const response = await fetch('YOUR_API_ENDPOINT', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'multipart/form-data',
      },
    });

    const result = await response.json();
    
    if (!response.ok) {
      throw new Error(result.message || 'Upload failed');
    }

    return {
      success: true,
      url: result.url,
    };

  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
};