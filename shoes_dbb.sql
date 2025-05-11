-- Create the shoes table
CREATE TABLE shoes (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) CHECK (brand IN ('Adidas', 'Nike', 'Puma')) NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    url VARCHAR(255) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255) NOT NULL
);

-- Insert a sample row
INSERT INTO shoes (brand, name, price, url, gender, description, image_url)
VALUES (
    'Adidas',
    'Adidas Ultraboost Light',
    180.00,
    'https://adidas.com/ultraboostlight',
    'male',
    'Experience epic energy with the new Ultraboost Light, our lightest Ultraboost ever.',
    'https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/123/Ultraboost_Light.jpg'
);