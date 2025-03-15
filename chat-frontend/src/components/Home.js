import React from 'react';

const Home = () => {
    return (
        <div style={styles.container}>
            <h1>Welcome to the Chatbot Website</h1>
            <p>This is the home page. Navigate to the Chat page to interact with the AI chatbot.</p>
        </div>
    );
};

const styles = {
    container: {
        padding: '20px',
        textAlign: 'center',
    },
};

export default Home;