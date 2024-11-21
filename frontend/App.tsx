import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StatusBar } from 'react-native';

// Import screens
import HomeScreen from './src/screens/HomeScreen';
import WardrobeScreen from './src/screens/WardrobeScreen';
import OutfitPlannerScreen from './src/screens/OutfitPlannerScreen';
import RecommendationsScreen from './src/screens/RecommendationsScreen';

// Define custom theme
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#2c3e50',
    secondary: '#3498db',
    background: '#f8f9fa',
    surface: '#ffffff',
    error: '#e74c3c',
    onSurface: '#2c3e50',
    backdrop: 'rgba(0, 0, 0, 0.5)',
    disabled: '#95a5a6',
    placeholder: '#bdc3c7',
  },
  roundness: 8,
};

// Define navigation types
export type RootStackParamList = {
  Home: undefined;
  Wardrobe: undefined;
  OutfitPlanner: undefined;
  Recommendations: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

const App: React.FC = () => {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <PaperProvider theme={theme}>
          <NavigationContainer>
            <StatusBar
              barStyle="dark-content"
              backgroundColor={theme.colors.background}
            />
            <Stack.Navigator
              initialRouteName="Home"
              screenOptions={{
                headerStyle: {
                  backgroundColor: theme.colors.primary,
                },
                headerTintColor: '#fff',
                headerTitleStyle: {
                  fontWeight: 'bold',
                },
                animation: 'slide_from_right',
              }}>
              <Stack.Screen
                name="Home"
                component={HomeScreen}
                options={{
                  title: 'Fashion Assistant',
                }}
              />
              <Stack.Screen
                name="Wardrobe"
                component={WardrobeScreen}
                options={{
                  title: 'My Wardrobe',
                }}
              />
              <Stack.Screen
                name="OutfitPlanner"
                component={OutfitPlannerScreen}
                options={{
                  title: 'Outfit Planner',
                }}
              />
              <Stack.Screen
                name="Recommendations"
                component={RecommendationsScreen}
                options={{
                  title: 'Recommendations',
                }}
              />
            </Stack.Navigator>
          </NavigationContainer>
        </PaperProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
};

export default App;
