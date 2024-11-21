import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Image, Dimensions } from 'react-native';
import { Text, Card, Button, useTheme, Portal, Modal, IconButton } from 'react-native-paper';
import { Calendar, DateData } from 'react-native-calendars';
import { format } from 'date-fns';

// Types
interface Outfit {
  id: string;
  date: string;
  items: {
    top: ClothingItem;
    bottom: ClothingItem;
    shoes: ClothingItem;
    accessories?: ClothingItem[];
  };
  occasion: string;
}

interface ClothingItem {
  id: string;
  name: string;
  category: string;
  imageUri: string;
}

const OutfitPlannerScreen: React.FC = () => {
  const theme = useTheme();
  const [selectedDate, setSelectedDate] = useState<string>(format(new Date(), 'yyyy-MM-dd'));
  const [isModalVisible, setIsModalVisible] = useState(false);

  // Placeholder outfits data
  const [outfits] = useState<Record<string, Outfit>>({
    '2024-11-16': {
      id: '1',
      date: '2024-11-16',
      items: {
        top: {
          id: 't1',
          name: 'White T-Shirt',
          category: 'Tops',
          imageUri: 'https://images.jackjones.com/12255176/4482191/001/jackjones-jprblaharveyteesscrewneckzcph-white.png?v=56e87df228c31b9c4299db68a27d15ba',
        },
        bottom: {
          id: 'b1',
          name: 'Blue Jeans',
          category: 'Bottoms',
          imageUri: 'https://coach.scene7.com/is/image/Coach/cq227_p9j_a0?$mobileProductV3$',
        },
        shoes: {
          id: 's1',
          name: 'Sneakers',
          category: 'Shoes',
          imageUri: 'https://freshlypicked.com/cdn/shop/products/White_Stairs_2.jpg?v=1569299996',
        },
      },
      occasion: 'Casual',
    },
    '2024-11-17': {
      id: '2',
      date: '2024-11-17',
      items: {
        top: {
          id: 't2',
          name: 'Blue Shirt',
          category: 'Tops',
          imageUri: 'https://static.fursac.com/data/shirt-men-casual-shirts-blue-h3efab-eh05-d028-pl9830983.1720616505.jpg',
        },
        bottom: {
          id: 'b2',
          name: 'Black Pants',
          category: 'Bottoms',
          imageUri: 'https://media.gq.com/photos/665a26c1f068596faedb52cb/3:4/w_748%2Cc_limit/Straight-Leg%2520Cotton%2520and%2520Linen-Blend%2520Twill%2520Trousers.png',
        },
        shoes: {
          id: 's2',
          name: 'Dress Shoes',
          category: 'Shoes',
          imageUri: 'https://thursdayboots.com/cdn/shop/products/1024x1024-Men-Executive-Black-061821-3.4_1024x1024.jpg?v=1624034468',
        },
      },
      occasion: 'Formal',
    },
  });

  // Generate marked dates for calendar
  const markedDates = Object.keys(outfits).reduce((acc, date) => {
    acc[date] = {
      marked: true,
      dotColor: theme.colors.primary,
    };
    if (date === selectedDate) {
      acc[date] = {
        ...acc[date],
        selected: true,
        selectedColor: theme.colors.primary,
      };
    }
    return acc;
  }, {} as Record<string, any>);

  const handleDayPress = (day: DateData) => {
    setSelectedDate(day.dateString);
  };

  const renderOutfitCard = (outfit?: Outfit) => {
    if (!outfit) {
      return (
        <Card style={styles.outfitCard}>
          <Card.Content style={styles.emptyOutfitContent}>
            <Text variant="bodyLarge">No outfit planned for this day</Text>
            <Button
              mode="contained"
              onPress={() => setIsModalVisible(true)}
              style={styles.planButton}
            >
              Plan Outfit
            </Button>
          </Card.Content>
        </Card>
      );
    }

    return (
      <Card style={styles.outfitCard}>
        <Card.Title
          title={`Outfit for ${format(new Date(outfit.date), 'MMMM d, yyyy')}`}
          subtitle={outfit.occasion}
          right={(props) => (
            <IconButton
              {...props}
              icon="pencil"
              onPress={() => setIsModalVisible(true)}
            />
          )}
        />
        <Card.Content>
          <View style={styles.outfitGrid}>
            <View style={styles.outfitItem}>
              <Image
                source={{ uri: outfit.items.top.imageUri }}
                style={styles.itemImage}
              />
              <Text variant="bodyMedium">{outfit.items.top.name}</Text>
            </View>
            <View style={styles.outfitItem}>
              <Image
                source={{ uri: outfit.items.bottom.imageUri }}
                style={styles.itemImage}
              />
              <Text variant="bodyMedium">{outfit.items.bottom.name}</Text>
            </View>
            <View style={styles.outfitItem}>
              <Image
                source={{ uri: outfit.items.shoes.imageUri }}
                style={styles.itemImage}
              />
              <Text variant="bodyMedium">{outfit.items.shoes.name}</Text>
            </View>
          </View>
        </Card.Content>
      </Card>
    );
  };

  return (
    <View style={[styles.container, { backgroundColor: theme.colors.background }]}>
      <ScrollView style={styles.scrollView}>
        <Calendar
          style={styles.calendar}
          theme={{
            todayTextColor: theme.colors.primary,
            selectedDayBackgroundColor: theme.colors.primary,
            arrowColor: theme.colors.primary,
          }}
          markedDates={markedDates}
          onDayPress={handleDayPress}
        />
        {renderOutfitCard(outfits[selectedDate])}
      </ScrollView>

      <Portal>
        <Modal
          visible={isModalVisible}
          onDismiss={() => setIsModalVisible(false)}
          contentContainerStyle={[
            styles.modal,
            { backgroundColor: theme.colors.background }
          ]}
        >
          <Text variant="headlineSmall" style={styles.modalTitle}>
            Plan Outfit for {format(new Date(selectedDate), 'MMMM d, yyyy')}
          </Text>
          {/* Placeholder for outfit planning form */}
          <Text variant="bodyMedium">
            Outfit planning form will go here...
          </Text>
          <Button
            mode="contained"
            onPress={() => setIsModalVisible(false)}
            style={styles.modalButton}
          >
            Close
          </Button>
        </Modal>
      </Portal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  calendar: {
    marginBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  outfitCard: {
    margin: 16,
    elevation: 4,
  },
  emptyOutfitContent: {
    alignItems: 'center',
    padding: 20,
  },
  planButton: {
    marginTop: 16,
  },
  outfitGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'wrap',
    gap: 16,
  },
  outfitItem: {
    alignItems: 'center',
    width: Dimensions.get('window').width / 3.8,
  },
  itemImage: {
    width: '100%',
    aspectRatio: 1,
    borderRadius: 8,
    marginBottom: 8,
  },
  modal: {
    padding: 20,
    margin: 20,
    borderRadius: 8,
  },
  modalTitle: {
    marginBottom: 16,
    textAlign: 'center',
  },
  modalButton: {
    marginTop: 16,
  },
});

export default OutfitPlannerScreen;