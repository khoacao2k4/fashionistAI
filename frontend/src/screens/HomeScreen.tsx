import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Platform, Alert, Image } from 'react-native';
import { Card, Title, Paragraph, Button, Portal, Modal, useTheme, ActivityIndicator, TextInput } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import * as ImagePicker from 'expo-image-picker';
import { SafeAreaView } from 'react-native-safe-area-context';

const API_URL = 'https://447f-72-33-2-244.ngrok-free.app';

type HomeScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Home'>;
};

type ImageInfo = {
  uri: string;
  type?: string;
  fileName?: string;
};

type PredictionResponse = {
  image_id: string;
  subCategory: string;
  articleType: string;
  baseColour: string;
  season: string;
  usage: string;
};

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const theme = useTheme();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedImage, setSelectedImage] = useState<ImageInfo | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [editedPrediction, setEditedPrediction] = useState<PredictionResponse | null>(null);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);



  const features = [
    {
      title: 'My Wardrobe',
      description: 'Organize and manage your clothing collection',
      icon: 'hanger',
      screen: 'Wardrobe',
    },
    {
      title: 'Outfit Planner',
      description: 'Create and plan your perfect outfits',
      icon: 'tshirt-crew',
      screen: 'OutfitPlanner',
    },
    {
      title: 'Style Recommendations',
      description: 'Get personalized fashion suggestions',
      icon: 'lightbulb-outline',
      screen: 'Recommendations',
    },
  ];

  const requestPermissions = async () => {
    if (Platform.OS !== 'web') {
      const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
      const { status: libraryStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      
      if (cameraStatus !== 'granted' || libraryStatus !== 'granted') {
        Alert.alert(
          'Permission Required',
          'Please grant camera and photo library permissions to use this feature.',
          [{ text: 'OK' }]
        );
        return false;
      }
    }
    return true;
  };

  const pickImage = async (useCamera: boolean) => {
    const permissionGranted = await requestPermissions();
    if (!permissionGranted) return;

    try {
      const result = useCamera
        ? await ImagePicker.launchCameraAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 0.8,
          })
        : await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 0.8,
          });

      if (!result.canceled) {
        const asset = result.assets[0];
        setSelectedImage({
          uri: asset.uri,
          type: 'image/jpeg',
          fileName: asset.uri.split('/').pop(),
        });
        setIsModalVisible(false);
        handleImageUpload({
          uri: asset.uri,
          type: 'image/jpeg',
          fileName: asset.uri.split('/').pop(),
        });
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to select image');
      console.error(error);
    }
  };

    const updateMetadata = async (data: PredictionResponse) => {
      try {
        const updateResponse = await fetch(`${API_URL}/update_metadata`, {
          method: 'PUT',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updatePayload),
        });

        if (!updateResponse.ok) {
          throw new Error(`Metadata update failed: ${updateResponse.status}`);
        }

        Alert.alert(
          'Success',
          'Image details updated successfully!',
          [
            {
              text: 'View in Wardrobe',
              onPress: () => navigation.navigate('Wardrobe'),
            },
            { text: 'OK' },
          ]
        );
      } catch (error) {
        Alert.alert('Error', 'Failed to update metadata');
        console.error('Update metadata error:', error);
      }
    };

    const handleImageUpload = async (imageInfo: ImageInfo) => {
    try {
      setIsUploading(true);

      const formData = new FormData();
      formData.append('file', {
        uri: imageInfo.uri,
        type: imageInfo.type || 'image/jpeg',
        name: imageInfo.fileName || 'upload.jpg',
      } as any);

      const predictResponse = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (!predictResponse.ok) {
        throw new Error(`Prediction failed: ${predictResponse.status}`);
      }

      const predictionData = await predictResponse.json();
      
      // Ensure the predictionData has the required structure
      const formattedPrediction: PredictionResponse = {
        image_id: predictionData.image_id,
        subCategory: predictionData.subCategory || '',
        articleType: predictionData.articleType || '',
        baseColour: predictionData.baseColour || '',
        season: predictionData.season || '',
        usage: predictionData.usage || ''
      };

      setPrediction(formattedPrediction);
      setEditedPrediction(formattedPrediction);
      
      // No need to call updateMetadata here as we'll let the user edit first
      setIsEditModalVisible(true);
    } catch (error) {
      Alert.alert(
        'Error',
        `Failed to process image: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleEditSave = async () => {
    if (!editedPrediction || !prediction?.image_id) {
      Alert.alert('Error', 'No data to save');
      return;
    }

    try {
      // Start loading state if you want to show a loading indicator
      setIsUploading(true);

      const updatePayload = {
        image_id: prediction.image_id,
        subCategory: editedPrediction.subCategory,
        articleType: editedPrediction.articleType,
        baseColour: editedPrediction.baseColour,
        season: editedPrediction.season,
        usage: editedPrediction.usage
      };

      const updateResponse = await fetch(`${API_URL}/update_metadata`, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_id: prediction.image_id,
          subCategory: editedPrediction.subCategory,
          articleType: editedPrediction.articleType,
          baseColour: editedPrediction.baseColour,
          season: editedPrediction.season,
          usage: editedPrediction.usage
        }),
      });

      if (!updateResponse.ok) {
        const errorData = await updateResponse.text();
        throw new Error(`Failed to update: ${updateResponse.status} - ${errorData}`);
      }

      // Update local state with the edited prediction
      setPrediction(editedPrediction);
      
      // Close the edit modal
      setIsEditModalVisible(false);
      
      // Show success message with options
      Alert.alert(
        'Success',
        'Item added to wardrobe successfully!',
        [
          {
            text: 'View in Wardrobe',
            onPress: () => navigation.navigate('Wardrobe'),
          },
          { text: 'Add Another', onPress: () => {
            setSelectedImage(null);
            setPrediction(null);
            setEditedPrediction(null);
          }},
        ]
      );
    } catch (error) {
      Alert.alert(
        'Error',
        `Failed to save changes: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
      console.error('Save error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleTextInputChange = (field: keyof PredictionResponse, value: string) => {
    setEditedPrediction(prev => 
      prev ? { ...prev, [field]: value } : null
    );
  };

  const renderEditModal = () => (
    <Portal>
      <Modal
        visible={isEditModalVisible}
        onDismiss={() => setIsEditModalVisible(false)}
        contentContainerStyle={styles.editModalContent}
      >
        <ScrollView>
          <Title style={styles.modalTitle}>Edit Details</Title>
          
          <TextInput
            label="Category"
            value={editedPrediction?.subCategory || ''}
            onChangeText={(text: string) => handleTextInputChange('subCategory', text)}
            style={styles.input}
          />
          
          <TextInput
            label="Type"
            value={editedPrediction?.articleType || ''}
            onChangeText={(text: string) => handleTextInputChange('articleType', text)}
            style={styles.input}
          />
          
          <TextInput
            label="Color"
            value={editedPrediction?.baseColour || ''}
            onChangeText={(text: string) => handleTextInputChange('baseColour', text)}
            style={styles.input}
          />
          
          <TextInput
            label="Season"
            value={editedPrediction?.season || ''}
            onChangeText={(text: string) => handleTextInputChange('season', text)}
            style={styles.input}
          />
          
          <TextInput
            label="Usage"
            value={editedPrediction?.usage || ''}
            onChangeText={(text: string) => handleTextInputChange('usage', text)}
            style={styles.input}
          />

          <View style={styles.modalButtons}>
            <Button
              mode="contained"
              onPress={handleEditSave}
              style={styles.modalButton}
              disabled={isUploading}
            >
              {isUploading ? 'Saving...' : 'Save Changes'}
            </Button>
            <Button
              mode="outlined"
              onPress={() => setIsEditModalVisible(false)}
              style={styles.modalButton}
              disabled={isUploading}
            >
              Cancel
            </Button>
          </View>
        </ScrollView>
      </Modal>
    </Portal>
  );

  const renderPredictionDetails = () => {
    if (!prediction) return null;


    return (
      <View style={styles.predictionContainer}>
        <View style={styles.predictionHeader}>
          <Title style={styles.predictionTitle}>Classification Results</Title>
          <Button
            mode="contained"
            onPress={() => {
              console.log('Setting initial edited prediction:', prediction); // Debug log
              setEditedPrediction({...prediction}); // Create a new object to avoid reference issues
              setIsEditModalVisible(true);
            }}
            icon="pencil"
            style={styles.editButton}
          >
            Edit
          </Button>
        </View>
        <View style={styles.predictionDetails}>
          <Paragraph>Category: {prediction.subCategory}</Paragraph>
          <Paragraph>Type: {prediction.articleType}</Paragraph>
          <Paragraph>Color: {prediction.baseColour}</Paragraph>
          <Paragraph>Season: {prediction.season}</Paragraph>
          <Paragraph>Usage: {prediction.usage}</Paragraph>
        </View>
      </View>
    );
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.colors.background }}>
      <ScrollView style={styles.container}>
        <View style={styles.welcomeSection}>
          <Title style={styles.welcomeTitle}>StyleSnap</Title>
          <Paragraph style={styles.welcomeText}>
            Your personal stylist to help you look your best every day
          </Paragraph>
        </View>

        <Button
          mode="contained"
          onPress={() => setIsModalVisible(true)}
          style={styles.uploadButton}
          icon="camera-plus"
          disabled={isUploading}
        >
          {isUploading ? 'Uploading...' : 'Add New Item'}
        </Button>

        {isUploading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color={theme.colors.primary} />
            <Paragraph style={styles.loadingText}>Processing image...</Paragraph>
          </View>
        )}

        {selectedImage && (
          <View style={styles.previewContainer}>
            <Title style={styles.previewTitle}>Latest Upload</Title>
            <Image
              source={{ uri: selectedImage.uri }}
              style={styles.imagePreview}
            />
            {renderPredictionDetails()}  {/* Add this line */}
          </View>
        )}

        <View style={styles.featuresContainer}>
          {features.map((feature, index) => (
            <Card
              key={index}
              style={styles.card}
              onPress={() => navigation.navigate(feature.screen as keyof RootStackParamList)}
            >
              <Card.Content style={styles.cardContent}>
                <Icon
                  name={feature.icon}
                  size={32}
                  color={theme.colors.primary}
                  style={styles.icon}
                />
                <Title style={styles.cardTitle}>{feature.title}</Title>
                <Paragraph style={styles.cardDescription}>
                  {feature.description}
                </Paragraph>
              </Card.Content>
            </Card>
          ))}
        </View>

        <Portal>
          <Modal
            visible={isModalVisible}
            onDismiss={() => setIsModalVisible(false)}
            contentContainerStyle={styles.modalContent}
          >
            <Title style={styles.modalTitle}>Add New Item</Title>
            <Button
              mode="contained"
              onPress={() => pickImage(true)}
              style={styles.modalButton}
              icon="camera"
            >
              Take Photo
            </Button>
            <Button
              mode="contained"
              onPress={() => pickImage(false)}
              style={styles.modalButton}
              icon="image"
            >
              Choose from Gallery
            </Button>
            <Button
              mode="outlined"
              onPress={() => setIsModalVisible(false)}
              style={styles.modalButton}
            >
              Cancel
            </Button>
          </Modal>
        </Portal>
        {renderEditModal()}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  loadingContainer: {
    alignItems: 'center',
    marginVertical: 20,
  },
  loadingText: {
    marginTop: 10,
  },
  predictionContainer: {
    marginTop: 16,
    padding: 16,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    width: '100%',
  },
  predictionTitle: {
    fontSize: 18,
    marginBottom: 12,
    textAlign: 'center',
  },
  predictionDetails: {
    gap: 8,
  },
    editModalContent: {
    backgroundColor: 'white',
    padding: 20,
    margin: 20,
    borderRadius: 8,
    maxHeight: '80%',
  },
  input: {
    marginBottom: 16,
  },
  modalButtons: {
    flexDirection: 'column',
    gap: 10,
    marginTop: 16,
  },
  predictionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  editButton: {
    paddingHorizontal: 8,
  },
  container: {
    flex: 1,
    padding: 16,
  },
  welcomeSection: {
    marginBottom: 24,
    alignItems: 'center',
  },
  welcomeTitle: {
    fontSize: 24,
    marginBottom: 8,
  },
  welcomeText: {
    fontSize: 16,
    textAlign: 'center',
  },
  uploadButton: {
    marginBottom: 16,
  },
  previewContainer: {
    marginBottom: 24,
    alignItems: 'center',
  },
  previewTitle: {
    fontSize: 18,
    marginBottom: 8,
  },
  imagePreview: {
    width: 200,
    height: 150,
    borderRadius: 8,
  },
  featuresContainer: {
    gap: 16,
  },
  card: {
    marginBottom: 16,
  },
  cardContent: {
    alignItems: 'center',
    padding: 16,
  },
  icon: {
    marginBottom: 8,
  },
  cardTitle: {
    fontSize: 18,
    marginBottom: 8,
    textAlign: 'center',
  },
  cardDescription: {
    textAlign: 'center',
  },
  modalContent: {
    backgroundColor: 'white',
    padding: 20,
    margin: 20,
    borderRadius: 8,
  },
  modalTitle: {
    textAlign: 'center',
    marginBottom: 20,
  },
  modalButton: {
    marginBottom: 10,
  },
});

export default HomeScreen;