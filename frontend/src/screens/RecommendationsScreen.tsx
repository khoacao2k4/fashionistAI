import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
  Dimensions,
  ActivityIndicator,
  TouchableOpacity,
} from 'react-native';

const { width } = Dimensions.get('window');

const API_URL = 'https://447f-72-33-2-244.ngrok-free.app';

const RecommendationsScreen: React.FC = () => {
  const [selectedOccasion, setSelectedOccasion] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const categories = ['Casual', 'Semi-Formal', 'Formal', 'Athletic'];

  const fetchRecommendations = async () => {
    if (!selectedOccasion) {
      Alert.alert('Error', 'Please select an occasion before proceeding.');
      return;
    }

    const payload = {
      occasion: selectedOccasion,
      n: 2,
    };

    try {
      setLoading(true);
      const response = await fetch(API_URL + '/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      Alert.alert('Success', `Recommendations received: ${JSON.stringify(data)}`);
    } catch (error) {
      Alert.alert(
        'Error',
        `Failed to fetch recommendations: ${
          error instanceof Error ? error.message : 'Unknown error'
        }`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.headerText}>Outfits brought to you by fashionistAI</Text>
      <View style={styles.gridContainer}>
        {categories.map((category) => (
          <TouchableOpacity
            key={category}
            style={[
              styles.categoryBox,
              selectedOccasion === category && styles.selectedBox,
            ]}
            onPress={() => setSelectedOccasion(category)}
          >
            <Text
              style={[
                styles.boxText,
                selectedOccasion === category && styles.selectedText,
              ]}
            >
              {category}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity
        style={styles.aiButton}
        onPress={fetchRecommendations}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator size="small" color="#fff" />
        ) : (
          <Text style={styles.aiButtonText}>AI Describe</Text>
        )}
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  headerText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    textAlign: 'center',
  },
  gridContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  categoryBox: {
    width: (width - 60) / 2,
    padding: 15,
    borderRadius: 8,
    marginBottom: 20,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f0f0f0',
  },
  selectedBox: {
    backgroundColor: '#007AFF',
  },
  boxText: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  selectedText: {
    color: '#fff',
    fontWeight: '700',
  },
  aiButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  aiButtonText: {
    fontSize: 18,
    color: '#fff',
    fontWeight: '600',
  },
});

export default RecommendationsScreen;
