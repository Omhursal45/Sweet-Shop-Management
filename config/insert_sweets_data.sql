-- Correct SQL to insert sweets data into sweetshop database
-- Make sure you run: USE sweetshop; first

USE sweetshop;

-- Insert sweets data (image field is NULL since it's optional)
INSERT INTO sweets_sweet (id, name, category, price, quantity, description, created_at, updated_at, image) VALUES
(UUID(), 'Ladoo', 'Sweet', 100.00, 10, 'Traditional Indian sweet made from gram flour.', NOW(), NOW(), NULL),
(UUID(), 'Gulab Jamun', 'Sweet', 120.00, 15, 'Soft milk-solid balls soaked in sugar syrup.', NOW(), NOW(), NULL),
(UUID(), 'Rasgulla', 'Sweet', 110.00, 20, 'Spongy cottage cheese balls in sugar syrup.', NOW(), NOW(), NULL),
(UUID(), 'Jalebi', 'Sweet', 80.00, 25, 'Crispy orange-colored sweet pretzels soaked in sugar syrup.', NOW(), NOW(), NULL),
(UUID(), 'Barfi', 'Sweet', 150.00, 12, 'Dense milk-based sweet with various flavors.', NOW(), NOW(), NULL),
(UUID(), 'Kaju Katli', 'Sweet', 200.00, 8, 'Diamond-shaped cashew fudge.', NOW(), NOW(), NULL),
(UUID(), 'Peda', 'Sweet', 130.00, 18, 'Soft, milk-based sweet with cardamom flavor.', NOW(), NOW(), NULL),
(UUID(), 'Mysore Pak', 'Sweet', 140.00, 14, 'Rich, ghee-laden sweet from South India.', NOW(), NOW(), NULL),
(UUID(), 'Soan Papdi', 'Sweet', 90.00, 22, 'Flaky, layered sweet with a melt-in-mouth texture.', NOW(), NOW(), NULL),
(UUID(), 'Rasmalai', 'Sweet', 160.00, 10, 'Soft cheese patties in sweetened, thickened milk.', NOW(), NOW(), NULL),
(UUID(), 'Modak', 'Sweet', 100.00, 16, 'Sweet dumplings filled with coconut and jaggery.', NOW(), NOW(), NULL),
(UUID(), 'Chikki', 'Sweet', 70.00, 30, 'Brittle made from nuts and jaggery or sugar.', NOW(), NOW(), NULL),
(UUID(), 'Balushahi', 'Sweet', 95.00, 20, 'Flaky, glazed doughnut-like sweet.', NOW(), NOW(), NULL),
(UUID(), 'Kheer', 'Sweet', 85.00, 15, 'Rice pudding with milk, sugar, and cardamom.', NOW(), NOW(), NULL),
(UUID(), 'Imarti', 'Sweet', 75.00, 25, 'Deep-fried, flower-shaped sweet in sugar syrup.', NOW(), NOW(), NULL),
(UUID(), 'Kalakand', 'Sweet', 145.00, 12, 'Dense, milk-based sweet with a grainy texture.', NOW(), NOW(), NULL),
(UUID(), 'Petha', 'Sweet', 60.00, 35, 'Candied ash gourd, translucent and sweet.', NOW(), NOW(), NULL),
(UUID(), 'Gajar Halwa', 'Sweet', 125.00, 10, 'Carrot pudding cooked in milk and ghee.', NOW(), NOW(), NULL),
(UUID(), 'Milk Cake', 'Sweet', 180.00, 8, 'Rich, fudge-like sweet made from milk solids.', NOW(), NOW(), NULL),
(UUID(), 'Lassi', 'Sweet', 50.00, 40, 'Yogurt-based drink, sweet or salty.', NOW(), NOW(), NULL);

