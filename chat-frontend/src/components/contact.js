import React from 'react';

const Contact = () => {
    return (
        <div style={styles.container}>
            <h1>Contact Us</h1>
            <p>Email: support@chatbot.com</p>
            <p>Phone: +1 123 456 7890</p>
        </div>
    );
};

const styles = {
    container: {
        padding: '20px',
        textAlign: 'center',
    },
};

export default Contact;