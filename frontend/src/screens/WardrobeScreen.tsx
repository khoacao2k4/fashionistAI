import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Card, Title, Text, useTheme, IconButton, ActivityIndicator } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Swipeable, ScrollView } from 'react-native-gesture-handler';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';

// Updated type to match API response
type ClothingItem = {
  _id: string;
  subCategory: string;
  article: string;
  baseColour: string;
  season: string;
  usage: string;
  image: string; // base64 string
};

type WardrobeScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Wardrobe'>;
};

const API_URL = 'https://447f-72-33-2-244.ngrok-free.app';

const WardrobeScreen: React.FC<WardrobeScreenProps> = ({ navigation }) => {
  const theme = useTheme();
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [clothes, setClothes] = useState<ClothingItem[]>([]);

  const loadClothes = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/get_all`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (Array.isArray(data)) {
        setClothes(data);
      } else if (data.error) {
        throw new Error(data.error);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      Alert.alert(
        'Error',
        'Failed to load wardrobe items: ' + (error instanceof Error ? error.message : 'Unknown error')
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadClothes();
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadClothes();
    setRefreshing(false);
  };

  const deleteClothingItem = async (item: ClothingItem) => {
    try {
      const response = await fetch(`${API_URL}/delete_image`, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_id: item.image
        })
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`Failed to delete: ${response.status} - ${errorData}`);
      }

      const data = await response.json();
      console.log('Delete response:', data);

      // Update local state to remove the deleted item
      setClothes(prevClothes => prevClothes.filter(clothingItem => clothingItem.id !== item._id));

      Alert.alert(
        'Success',
        'Item removed from wardrobe successfully'
      );
    } catch (error) {
      console.error('Delete error:', error);
      Alert.alert(
        'Error',
        `Failed to delete item: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
    }
  };

  const renderRightActions = (item: ClothingItem) => {
    return (
      <View style={styles.deleteAction}>
        <IconButton
          icon="delete"
          iconColor="white"
          size={24}
          onPress={() => {
            Alert.alert(
              'Delete Item',
              'Are you sure you want to remove this item from your wardrobe?',
              [
                { text: 'Cancel', style: 'cancel' },
                { text: 'Delete', onPress: () => deleteClothingItem(item), style: 'destructive' }
              ]
            );
          }}
        />
      </View>
    );
  };

  const renderItem = (item: ClothingItem) => {
    return (
      <Swipeable
        key={item._id}
        renderRightActions={() => renderRightActions(item)}
        overshootRight={false}
      >
        <Card style={styles.card}>
          <Card.Cover 
            source={{ uri: `data:image/jpeg;base64,${item.image}` }} 
            style={styles.cardImage}
          />
          <Card.Content>
            <Title>{item.subCategory}</Title>
            <Text variant="bodyMedium">{item.article}</Text>
            <View style={styles.detailsContainer}>
              <Text variant="bodySmall" style={styles.detail}>
                Color: {item.baseColour}
              </Text>
              <Text variant="bodySmall" style={styles.detail}>
                Season: {item.season}
              </Text>
              <Text variant="bodySmall" style={styles.detail}>
                Usage: {item.usage}
              </Text>
            </View>
          </Card.Content>
        </Card>
      </Swipeable>
    );
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: theme.colors.background }]}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContentContainer}
        onRefresh={handleRefresh}
        refreshing={refreshing}
      >
        {clothes.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Text>No items in your wardrobe yet.</Text>
          </View>
        ) : (
          clothes.map(renderItem)
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  scrollContentContainer: {
    padding: 16,
    gap: 16,
  },
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  cardImage: {
    height: 200,
    resizeMode: 'cover',
  },
  detailsContainer: {
    marginTop: 8,
    gap: 4,
  },
  detail: {
    color: '#666',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  deleteAction: {
    backgroundColor: '#dc3545',
    justifyContent: 'center',
    alignItems: 'center',
    width: 80,
    height: '100%',
    borderTopRightRadius: 8,
    borderBottomRightRadius: 8,
  },
});

export default WardrobeScreen;