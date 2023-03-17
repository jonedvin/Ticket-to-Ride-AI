This project is dedicated to creating an almost-independent AI for real-life rounds of the popular board game Ticket to Ride! It works as an additional player on a physical board, and takes its input from one of the players. It is designed to be as easy to use as possible.

The AI uses tickets found in the 1912 expansion pack, so that its tickets won't crash with the players.

Usage:
- Input player info, and click "Confirm"
- It says in the top left who's turn it is
- Whenever a player makes a move, input the move into the AI's interface. 
   '- If the player drew a card, click the "Draw cards" button
   '- If they bought a route, click the route they bought, and the map will update. If it doesn't click a different spot on the same route.
- When it's the AI's turn, it will do its move automatically. When it's done, the turn in the top left will say the next player's name. You can now read the last action of the AI on the right side of the screen. If it bought a route, you should find it on the map and add the trains to the physical game board.




TODO:
- Add button to finish the game
- Add buttons to add trains to players (so we don't have to count trains before starting)
- Add AI tickets to result screen
- Add undo button
- Deal with destinations being impossible to reach


OPTIMIZATIONS:
- Optimize find possible routes
    '- expanding max distance
    '- A*
- Only buy tickets if there's more than X trains left for each player
- Don't try tunnels unless you have an extra card
- Ranger ruter etter hvor lang omvei man får hvis man ikke kjøper den
- AI should prioritize using locomotives where they're necessary
- Make AI.draw_tickets combine tickets if more than one is to be drawn
- Improve ticket complete check -> store ticket path?
- Look for better way of stopping all recursive calls of function
- Smarter usage of cards on hand
- Buy routes based on opponents predicted path
- Add AI personality (TicketTrainLimit, longest route tactics etc., prioritize length vs points)
