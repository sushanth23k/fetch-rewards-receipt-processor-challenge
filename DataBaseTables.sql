-- Create the receipts table
CREATE TABLE fetch_buffalodug.receipts (
    id CHAR(36) PRIMARY KEY,
    retailer VARCHAR(255) NOT NULL,
    purchaseDate DATE NOT NULL,
    purchaseTime TIME NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    points INT DEFAULT 0 -- Column to store points awarded for the receipt
);

-- Create the items table
CREATE TABLE fetch_buffalodug.items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_id CHAR(36),
    shortDescription VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (receipt_id) REFERENCES fetch_buffalodug.receipts(id) ON DELETE CASCADE
);
