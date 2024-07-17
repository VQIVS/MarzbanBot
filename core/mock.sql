-- PostgreSQL Database Credentials
-- Make sure to replace these with your actual credentials when running in PostgreSQL

-- Configuration model
INSERT INTO website_configuration (panel_username, panel_password, bot_name, bot_url, panel_url, token)
VALUES ('panel_user', 'panel_password', 'My Bot', 'https://example.com/bot', 'https://example.com/panel', 'your_bot_token_here');

-- Product model
INSERT INTO website_product (name, price, data_limit, expire)
VALUES ('Product 1', 100, 1024, NULL),
       ('Product 2', 50, 512, 30);

-- TelegramChannel model
INSERT INTO website_telegramchannel (name, title, address)
VALUES ('Channel 1', 'Channel Title 1', '@channel1'),
       ('Channel 2', 'Channel Title 2', '@channel2');

-- Tutorial model
INSERT INTO website_tutorial (name, telegram_id)
VALUES ('Tutorial 1', '123456789'),
       ('Tutorial 2', '987654321');

-- ChannelAdmin model
INSERT INTO website_channeladmin (name, telegram_id)
VALUES ('Admin 1', 'admin1_telegram_id'),
       ('Admin 2', 'admin2_telegram_id');

-- Message model
INSERT INTO website_message (subject, text)
VALUES ('Message Subject 1', 'Message Text 1'),
       ('Message Subject 2', 'Message Text 2');

-- PaymentMethod model
INSERT INTO website_paymentmethod (holders_name, card_number)
VALUES ('Holder 1', '1111-2222-3333-4444'),
       ('Holder 2', '5555-6666-7777-8888');

-- Payment model
INSERT INTO website_payment (amount, photo, timestamp)
VALUES (100.00, '/path/to/photo1.jpg', NOW()),
       (50.00, '/path/to/photo2.jpg', NOW());

-- MajorProduct model
INSERT INTO website_majorproduct (name, price, data_limit, expire)
VALUES ('Major Product 1', 200, 2048, NULL),
       ('Major Product 2', 150, 1024, 30);

-- BotUser model
INSERT INTO bot_botuser (user_id, test_status, is_banned, status, state, selected_product_id, invited_by, has_received_prize, created_at, updated_at)
VALUES
    (1, 'Test Status 1', FALSE, 'Status 1', 'State 1', 1, NULL, FALSE, NOW(), NOW()),
    (2, 'Test Status 2', TRUE, 'Status 2', 'State 2', 2, 1, TRUE, NOW(), NOW());

-- Subscription model
INSERT INTO bot_subscription (user_id_id, sub_user, status, created_at, updated_at)
VALUES
    (1, 'Subscription User for 1', TRUE, NOW(), NOW()),
    (2, 'Subscription User for 2', FALSE, NOW(), NOW());

-- Order model
INSERT INTO bot_order (user_id_id, product_id, order_id, major_product_id, quantity, status, created_at, updated_at)
VALUES
    (1, 1, 'order_id_1', 1, 5, 'Pending', NOW(), NOW()),
    (2, 2, 'order_id_2', 2, 3, 'Completed', NOW(), NOW());
