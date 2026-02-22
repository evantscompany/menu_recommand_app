import React from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import { styles } from './CommonLoadingStyle';

const CommonLoading = ({ message = "데이터를 불러오고 있습니다..." }) => {
  return (
    <View style={styles.overlay}>
      <View style={styles.loadingBox}>
        <ActivityIndicator size="large" color="#6366F1" />
        <Text style={styles.messageText}>{message}</Text>
      </View>
    </View>
  );
};

export default CommonLoading;