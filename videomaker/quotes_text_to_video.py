from moviepy.editor import *
import os
import random

IMAGEMAGICK_BINARY = r"convert.exe"
# Create a directory to store output files
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


mp3files = os.listdir("natureaudio")
mp4files = os.listdir("naturevideo")
color = [
    (64, 28, 29),
    (99, 32, 7),
    (98, 32, 8),
    (33, 28, 25),
    (29, 31, 69),
    (76, 3, 72)

]
# Process each quote


def wrap_text(text, max_line_length):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) <= max_line_length:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


# Process each quote
quotesArray = [
    {
        "author": "Pseudonymous Bosch",
        "quote": "Books can also provoke emotions. And emotions sometimes are even more troublesome than ideas. Emotions have led people to do all sorts of things they later regret- like, oh, throwing a book at someone else."
    },
    {
        "author": "Chris Brown",
        "quote": "Haters keep on hating cause somebody's gotta do it."
    },
    {
        "author": "Chris Brown",
        "quote": "Haters keep on hating cause somebody's gotta do it."
    },
    {
        "author": "Anonymous",
        "quote": "When it rains, look for rainbows. When it's dark, look for stars."
    },
    {
        "author": "Jon Kabat Zinn",
        "quote": "You can't stop the waves, but you can learn to swim."
    },
    {
        "author": "Ralph Waldo Emerson",
        "quote": "For every minute you are angry you lose sixty seconds of happiness."
    },
    {
        "author": "Sora (No Game No Life)",
        "quote": "Life is not a game of luck. If you wanna win, work hard."
    },
    {
        "author": "Milton Berle",
        "quote": "If opportunity doesn't knock, build a door."
    },
    {
        "author": "A.J. Cronin",
        "quote": "Worry never robs tomorrow of its sorrow; it only saps today of its strength."
    },
    {
        "author": "Neale Donald Walsch",
        "quote": "Life begins at the end of your comfort zone."
    },
    {
        "author": "Mufti Menk",
        "quote": "My heart is too valuable to allow hatred and jealousy to rent a spot."
    },
    {
        "author": "Toni Morrison",
        "quote": "Definitions belong to the definers, not the defined."
    },
    {
        "author": "Mark A. Cooper",
        "quote": "Life has no remote. Get up and change it yourself."
    },
    {
        "author": "Naomi Judd",
        "quote": "A dead end street is a good place to turn around."
    },
    {
        "author": "Anonymous",
        "quote": "Progress has little to do with speed, but much to do with direction."
    },
    {
        "author": "William James",
        "quote": "Act as if what you do makes a difference. It does."
    },
    {
        "author": "John A. Shedd",
        "quote": "Ships in the harbour are safe, but that's not what ships are built for."
    },
    {
        "author": "Marianne Cantwell",
        "quote": "Weaknesses are just strengths in the wrong environment."
    },
    {
        "author": "Dodinsky",
        "quote": "Be there for others, but never leave yourself behind."
    },
    {
        "author": "Tom Stoppard",
        "quote": "Every exit is an entry somewhere else."
    },
    {
        "author": "Anna Quindlen",
        "quote": "Don't ever confuse the two, your life and your work. The second is only part of the first."
    },
    {
        "author": "Robert Louis Stevenson",
        "quote": "Don't judge each day by the harvest you reap but by the seeds that you plant."
    },
    {
        "author": "Saiki Michiru",
        "quote": "Knocking others down to gain an advantage is a fruitless endeavor. It means they've given up on winning any other way."
    },
    {
        "author": "Gray Fullbuster",
        "quote": "If you are looking back all the time, you'll never get ahead."
    },
    {
        "author": "Macklemore",
        "quote": "Change the game, don't let the game change you."
    },
    {
        "author": "Rabindranath Tagore",
        "quote": "Clouds come floating into my life, no longer to carry rain or usher storm, but to add color to my sunset sky."
    },
    {
        "author": "Goethe",
        "quote": "Everything is hard before it is easy."
    },
    {
        "author": "Marshall 'Blackbeard' D. Teach",
        "quote": "When you aim high, you sometimes come across fights not worth fighting."
    },
    {
        "author": "Nitya Prakash",
        "quote": "Make sure your worst enemy is not living between your own two ears."
    },
    {
        "author": "Dana White",
        "quote": "Nothing comes easy. Success doesn't just drop on your lap. You have to go out and fight for it every day."
    },
    {
        "author": "Jon Jones",
        "quote": "Look at those who have talked about you and doubted you. They are your inspirational reason to succeed."
    },
    {
        "author": "Khabib Nurmagomedov",
        "quote": "Climb the mountain so you can see the world, not so the world can see you."
    },
    {
        "author": "Anonymous",
        "quote": "Your problem isn't the problem. Your reaction is the problem."
    },
    {
        "author": "Elizabeth Barrett Browning",
        "quote": "Light tomorrow with today."
    },
    {
        "author": "Kyle Chandler",
        "quote": "Opportunity does not knock, it presents itself when you beat down the door."
    },
    {
        "author": "St. Jerome",
        "quote": "Good. Better. Best. Never let it rest. 'Til your good is better and your better is best."
    },
    {
        "author": "Vince Lombardi",
        "quote": "The only place where success comes before work is in the dictionary."
    },
    {
        "author": "Edith Wharton",
        "quote": "There are two ways of spreading light: to be the candle or the mirror that reflects it."
    },
    {
        "author": "Nicole Kidman",
        "quote": "Life has got all those twists and turns. You've got to hold on tight and off you go."
    },
    {
        "author": "Winston Churchill",
        "quote": "Attitude is the 'little' thing that makes a big difference."
    },
    {
        "author": "Herman Melville",
        "quote": "It is better to fail in originality than to succeed in imitation."
    },
    {
        "author": "Muhammad Ali",
        "quote": "Don't count the days, make the days count."
    },
    {
        "author": "Oscar Wilde",
        "quote": "The best way to appreciate your job is to imagine yourself without one."
    },
    {
        "author": "Paulo Coelho",
        "quote": "The world is changed by your example, not by your opinion."
    },
    {
        "author": "Rose Kennedy",
        "quote": "Life isn't a matter of milestones, but of moments."
    },
    {
        "author": "David T.S Wood",
        "quote": "Every master was once a disaster."
    },
    {
        "author": "Marian Wright Edelman",
        "quote": "You're not obligated to win. You're obligated to keep trying to do the best you can every day."
    },
    {
        "author": "Walter Elliot",
        "quote": "Perseverance is not a long race; it is many short races one after the other."
    },
    {
        "author": "Stephen King",
        "quote": "Talent is cheaper than table salt. What separates the talented individual from the successful one is a lot of hard work."
    },
    {
        "author": "Unknown",
        "quote": "Work until your bank account looks like a phone number."
    },
    {
        "author": "Vince Lombardi",
        "quote": "Perfection is not attainable. But if we chase perfection we can catch excellence."
    },
    {
        "author": "Jim Rohn",
        "quote": "Either you run the day or the day runs you."
    },
    {
        "author": "Walt Whitman",
        "quote": "Keep your face always toward the sunshine―and shadows will fall behind you."
    },
    {
        "author": "George Addair",
        "quote": "Everything you've ever wanted is on the other side of fear."
    },
    {
        "author": "Thomas Edison",
        "quote": "Opportunity is missed by most people because it is dressed in overalls and looks like work."
    },
    {
        "author": "Alexandra of The Productivity Zone",
        "quote": "It's not about better time management. It's about better life management."
    },
    {
        "author": "Tony Robbins",
        "quote": "Setting goals is the first step in turning the invisible into the visible."
    },
    {
        "author": "Will Rogers",
        "quote": "Don't let yesterday take up too much of today."
    },
    {
        "author": "Albert Einstein",
        "quote": "If A is a success in life, then A equals x plus y plus z. Work is x; y is play; and z is keeping your mouth shut."
    },
    {
        "author": "Stephen King",
        "quote": "Talent is cheaper than table salt. What separates the talented individual from the successful one is a lot of hard work."
    },
    {
        "author": "Henry Boye",
        "quote": "The most important trip you may take in life is meeting people halfway."
    },
    {
        "author": "Aldous Huxley",
        "quote": "There is only one corner of the universe you can be certain of improving, and that's your own self."
    },
    {
        "author": "Ruth E. Renkel",
        "quote": "Never fear shadows. They simply mean there's a light shining nearby."
    },
    {
        "author": "Truman Capote",
        "quote": "Failure is the condiment that gives success its flavor."
    },
    {
        "author": "Tom Stoppard",
        "quote": "Every exit is an entry somewhere else."
    },
    {
        "author": "Billie Jean King",
        "quote": "Champions keep playing until they get it right."
    },
    {
        "author": "Michele Ruiz",
        "quote": "If people are doubting how far you can go, go so far that you can't hear them anymore."
    },
    {
        "author": "Yiddish Proverb",
        "quote": "The truly rich are those who enjoy what they have."
    },
    {
        "author": "Marcus Aurelius",
        "quote": "Each day provides its own gifts."
    },
    {
        "author": "Walt Disney",
        "quote": "Get a good idea and stay with it. Dog it, and work at it until it's done right."
    },
    {
        "author": "Augustine Og Mandino",
        "quote": "Take the attitude of a student, never be too big to ask questions, never know too much to learn something new."
    },
    {
        "author": "Mary Anne Radmacher",
        "quote": "Courage doesn't always roar. Sometimes courage is a quiet voice at the end of the day saying, I will try again tomorrow. "
    },
    {
        "author": "Lucius Annaeus Seneca",
        "quote": "It is a rough road that leads to the heights of greatness."
    },
    {
        "author": "Unknown",
        "quote": "Resilience is when you address uncertainty with flexibility."
    },
    {
        "author": "Paul Bryant",
        "quote": "It's not the will to win that matters—everyone has that. It's the will to prepare to win that matters."
    },
    {
        "author": "Vernon Sanders Law",
        "quote": "Experience is a hard teacher because she gives the test first, the lesson afterwards."
    },
    {
        "author": "A.A. Milne",
        "quote": "Rivers know this: there is no hurry. We shall get there some day."
    },
    {
        "author": "Gordon B. Hinckley",
        "quote": "You cannot plow a field by turning it over in your mind. To begin, begin."
    },
    {
        "author": "Jessica Ennis",
        "quote": "The only one who can tell you 'you can't win' is you and you don't have to listen."
    },
    {
        "author": "Dolly Parton",
        "quote": "If you don't like the road you're walking, start paving another one."
    },
    {
        "author": "Diane von Furstenberg",
        "quote": "You carry the passport to your own happiness."
    },
    {
        "author": "Thomas Aquinas",
        "quote": "If the highest aim of a captain were to preserve his ship, he would keep it in port forever."
    },
    {
        "author": "Ruth Gordo",
        "quote": "Courage is like a muscle. We strengthen it by use."
    },
    {
        "author": "Pablo Picasso",
        "quote": "Inspiration does exist, but it must find you working."
    },
    {
        "author": "Mia Hamm",
        "quote": "Take your victories, whatever they may be, cherish them, use them, but don't settle for them."
    },
    {
        "author": "Robert Frost",
        "quote": "In three words I can sum up everything I've learned about life: It goes on."
    },
    {
        "author": "Confucius",
        "quote": "When it is obvious that goals can't be reached, don't adjust the goals, but adjust the action steps."
    },
    {
        "author": "Henry David Thoreau",
        "quote": "Happiness is like a butterfly; the more you chase it, the more it will elude you, but if you turn your attention to other things, it will come and sit softly on your shoulder."
    },
    {
        "author": "Alexander Graham Bell",
        "quote": "When one door closes, another opens; but we often look so long and so regretfully upon the closed door that we do not see the one that has opened for us."
    },
    {
        "author": "Sholom Aleichem",
        "quote": "Life is a dream for the wise, a game for the fool, a comedy for the rich, a tragedy for the poor."
    },
    {
        "author": "Michael Jordan",
        "quote": "You must expect great things of yourself before you can do them."
    },
    {
        "author": "Bill Clinton",
        "quote": "If you live long enough, you'll make mistakes. But if you learn from them, you'll be a better person."
    },
    {
        "author": "Kevin Kruse",
        "quote": "Life is about making an impact, not making an income."
    },
    {
        "author": "Emma Stone",
        "quote": "You're only human. You live once and life is wonderful, so eat the damned red velvet cupcake."
    },
    {
        "author": "Lillian Dickson",
        "quote": "Life is like a coin. You can spend it any way you wish, but you only spend it once."
    },
    {
        "author": "Forrest Gump",
        "quote": "My mama always said, life is like a box of chocolates. You never know what you're gonna get."
    },
    {
        "author": "Celine Dion",
        "quote": "Life imposes things on you that you can't control, but you still have the choice of how you're going to live through this."
    },
    {
        "author": "Kobe Bryant",
        "quote": "Everything negative – pressure, challenges – is all an opportunity for me to rise."
    },
    {
        "author": "Kevin Hart",
        "quote": "Everybody wants to be famous, but nobody wants to do the work. I live by that. You grind hard so you can play hard. At the end of the day, you put all the work in, and eventually it'll pay off. It could be in a year, it could be in 30 years. Eventually, your hard work will pay off."
    },
    {
        "author": "Dolly Parton",
        "quote": "The way I see it, if you want the rainbow, you gotta put up with the rain."
    },
    {
        "author": "Oprah Winfrey",
        "quote": "Turn your wounds into wisdom."
    },
    {
        "author": "Will Smith",
        "quote": "Money and success don't change people; they merely amplify what is already there."
    },
    {
        "author": "Colin Powell",
        "quote": "A dream doesn't become reality through magic; it takes sweat, determination and hard work."
    },
    {
        "author": "Jimmy Durante",
        "quote": "Be nice to people on the way up, because you may meet them on the way down."
    },
    {
        "author": "Martin Luther King, Jr.",
        "quote": "Life's most persistent and urgent question is, 'What are you doing for others?"
    },
    {
        "author": "Dean Karnazes",
        "quote": "Run when you can, walk if you have to, crawl if you must; just never give up."
    },
    {
        "author": "Rabindranath Tagore",
        "quote": "You can't cross the sea merely by standing and staring at the water."
    },
    {
        "author": "Epictetus",
        "quote": "The key is to keep company only with people who uplift you, whose presence calls forth your best."
    },
    {
        "author": "Thomas A. Edison",
        "quote": "Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time."
    },
    {
        "author": "St. Jerome",
        "quote": "Good, better, best. Never let it rest. 'Til your good is better and your better is best."
    },
    {
        "author": "Charles R. Swindoll",
        "quote": "Life is 10% what happens to you and 90% how you react to it."
    },
    {
        "author": "Elon Musk",
        "quote": "When something is important enough, you do it even if the odds are not in your favor."
    },
    {
        "author": "Louis Nizer",
        "quote": "A graceful taunt is worth a thousand insults."
    },
    {
        "author": "W. C. Fields",
        "quote": "Now don't say you can't swear off drinking; it's easy. I've done it a thousand times."
    },
    {
        "author": "Graham Greene",
        "quote": "In human relationships, kindness and lies are worth a thousand truths."
    },
    {
        "author": "Swami Vivekananda",
        "quote": "Truth can be stated in a thousand different ways, yet each one can be true."
    },
    {
        "author": "Henry David Thoreau",
        "quote": "There are a thousand hacking at the branches of evil to one who is striking at the root."
    },
    {
        "author": "John F. Kennedy",
        "quote": "Victory has a thousand fathers, but defeat is an orphan."
    },
    {
        "author": "Les Brown",
        "quote": "Too many of us are not living our dreams because we are living our fears."
    },
    {
        "author": "Pablo Neruda",
        "quote": "You can cut all the flowers but you cannot keep spring from coming."
    },
    {
        "author": "Marie Curie",
        "quote": "All my life through, the new sights of Nature made me rejoice like a child."
    },
    {
        "author": "Willie Nelson",
        "quote": "Once you replace negative thoughts with positive ones, you'll start having positive results."
    },
    {
        "author": "Zig Ziglar",
        "quote": "You don't have to be great to start, but you have to start to be great"
    },
    {
        "author": "Abu Bakr",
        "quote": "Good actions are a guard against the blows of adversity."
    },
    {
        "author": "Henry Ford",
        "quote": "Failure is simply the opportunity to begin again, this time more intelligently."
    },
    {
        "author": "Martin Luther King, Jr.",
        "quote": "Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that."
    },
    {
        "author": "Albert Einstein",
        "quote": "Weak people revenge. Strong people forgive. Intelligent People Ignore."
    },
    {
        "author": "Golda Meir",
        "quote": "One cannot and must not try to erase the past merely because it does not fit the present."
    },
    {
        "author": "Aristotle",
        "quote": "It is during our darkest moments that we must focus to see the light."
    },
    {
        "author": "Albert Einstein",
        "quote": "Common sense is the collection of prejudices acquired by age eighteen."
    },
    {
        "author": "Walt Whitman",
        "quote": "Charity and personal force are the only investments that are worth anything."
    },
    {
        "author": "Marie Curie",
        "quote": "Nothing in life is to be feared. It is only to be understood."
    },
    {
        "author": "Seneca",
        "quote": "You can tell the character of every man when you see how he receives praise."
    },
    {
        "author": "Jean Cocteau",
        "quote": "Tact in audacity consists in knowing how far we may go too far."
    },
    {
        "author": "Oliver Wendell Holmes, Jr.",
        "quote": "Taxes are what we pay for civilized society."
    },
    {
        "author": "Sir Winston Churchill",
        "quote": "Courage is rightly esteemed the first of human qualities because it is the quality which guarantees all others."
    },
    {
        "author": "Marcel Proust",
        "quote": "Just as those who practice the same profession recognize each other instinctively, so do those who practice the same vice."
    },
    {
        "author": "Leo Tolstoy",
        "quote": "All happy families resemble one another, but each unhappy family is unhappy in its own way."
    },
    {
        "author": "T.S. Eliot",
        "quote": "We had the experience but missed the meaning."
    },
    {
        "author": "Seneca",
        "quote": "What others think of us would be of little moment did it not, when known, so deeply tinge what we think of ourselves."
    },
    {
        "author": "Michel de Montaigne",
        "quote": "Not being able to govern events, I govern myself."
    },
    {
        "author": "Albert Camus ",
        "quote": "You know what charm is: a way of getting the answer yes without having asked any clear question."
    },
    {
        "author": "Henry David Thoreau",
        "quote": "Let your capital be simplicity and contentment."
    },
    {
        "author": "Robert Musil",
        "quote": "It's not the genius who is 100 years ahead of his time but average man who is 100 years behind it."
    },
    {
        "author": "Socrates",
        "quote": "To find yourself, think for yourself"
    },
    {
        "author": "Alexander Pope",
        "quote": "Do good by stealth, and blush to find it fame."
    },
    {
        "author": "Erich Fromm",
        "quote": "Love is the only sane and satisfactory answer to the problem of human existence."
    },
    {
        "author": "Norman Douglas",
        "quote": "You can tell the ideals of a nation by its advertisements."
    },
    {
        "author": "Stephen King",
        "quote": "Only enemies speak the truth; friends and lovers lie endlessly, caught in the web of duty."
    },
    {
        "author": "Bertrand Russell",
        "quote": "What is wanted is not the will to believe, but the will to find out, which is the exact opposite."
    },
    {
        "author": "Abraham Lincoln",
        "quote": "Most folks are about as happy as they make up their minds to be."
    },
    {
        "author": "P Henry",
        "quote": "The liberties of a people never were, nor ever will be, secure when the transactions of their rulers may be concealed from them."
    },
    {
        "author": "Voltaire",
        "quote": "It is dangerous to be right when the government is wrong."
    },
    {
        "author": "W.H. Auden",
        "quote": "I and the public know, what all schoolchildren learn, those to whom evil is done do evil in return."
    },
    {
        "author": "Benjamin Franklin",
        "quote": "Be always at war with your vices, at peace with your neighbors, and let each new year find you a better man."
    },
    {
        "author": "Nora Ephron",
        "quote": "Insane people are always sure that they are fine. It is only the sane people who are willing to admit that they are crazy."
    },
    {
        "author": "Desiderius Erasmus",
        "quote": "The summit of happiness is reached when a person is ready to be what he is."
    },
    {
        "author": "Theodor Seuss Geisel",
        "quote": "Be who you are and say what you feel 'cause people who mind don't matter, and people who matter don't mind."
    },
    {
        "author": "DH Lawrence",
        "quote": "Never trust the artist. Trust the tale. The proper function of the critic is to save the tale from the artist who created it."
    },
    {
        "author": "Jean Cocteau",
        "quote": "Nothing ever gets anywhere. The earth keeps turning round and gets nowhere. The moment is the only thing that counts."
    },
    {
        "author": "Thomas Szasz",
        "quote": "The stupid neither forgive nor forget; the naive forgive and forget; the wise forgive but do not forget."
    },
    {
        "author": "Leopold Kronecker",
        "quote": "God made integers, all else is the work of man."
    },
    {
        "author": "Robert Frost",
        "quote": "By working faithfully eight hours a day, you may eventually get to be a boss and work twelve hours a day."
    },
    {
        "author": "William Makepeace Thackeray",
        "quote": "Follow your honest convictions and be strong."
    },
    {
        "author": "Benjamin Disraeli",
        "quote": "Change is as inexorable as time, yet nothing meets with more resistance."
    },
    {
        "author": "Winston S. Churchill",
        "quote": "Success is not final; failure is not fatal: It is the courage to continue that counts."
    },
    {
        "author": "Alert von Szent-Gyorgy",
        "quote": "Discovery consists of seeing what everybody has seen and thinking what nobody has thought."
    },
    {
        "author": "William Penn",
        "quote": "Time is what we want most, but what we use worst."
    },
    {
        "author": "Marianne Williamson",
        "quote": "And no one will listen to us until we listen to ourselves."
    },
    {
        "author": "Jack Kornfield",
        "quote": "When we get too caught up in the busyness of the world we lose connection with one another and ourselves."
    },
    {
        "author": "Stephen R. Covey",
        "quote": "The key to the ability to change is a changeless sense of who you are, what you are about and what you value."
    },
    {
        "author": "Edward Young",
        "quote": "We are all born originals-   why is it so many of us die copies?"
    },
    {
        "author": "Hans Hofmann",
        "quote": "The ability to simplify means to eliminate the unnecessary so that the necessary may speak."
    },
    {
        "author": "Lyn St. James",
        "quote": "You accomplish victory step by step, not by leaps and bounds."
    },
    {
        "author": "Evan Esar",
        "quote": "Success is the good fortune that comes from aspiration, desperation, perspiration and inspiration."
    },
    {
        "author": "Eleanor Roosevelt",
        "quote": "Nobody can make you feel inferior without your permission."
    },
    {
        "author": "Abraham Lincoln",
        "quote": "Most of us are just about as happy as we make up our minds to be."
    },
    {
        "author": "George Eliot",
        "quote": "It's never too late to be what you might have been."
    },
    {
        "author": "F. Scott Fitzgerald",
        "quote": "Vitality shows not only in the ability to persist, but in the ability to start over."
    },
    {
        "author": "Mahatma Gandhi",
        "quote": "I want freedom for the full expression of my personality."
    },
    {
        "author": "Napoleon Hill",
        "quote": "Failure is nature's plan to prepare you for great responsibilities."
    },
    {
        "author": "Mark Twain",
        "quote": "Always do right. This will gratify some people and astonish the rest."
    },
    {
        "author": "Wayne Dyer",
        "quote": "Abundance is not something we acquire. It is something we tune into."
    },
    {
        "author": "Voltaire",
        "quote": "Every man is guilty of all the good he didn't do."
    },
    {
        "author": "Nelson Mandela",
        "quote": "Let freedom reign. The sun never set on so glorious a human achievement."
    },
    {
        "author": "Ralph Waldo Emerson",
        "quote": "Improve your spare moments and they will become the brightest gems in your life."
    },
    {
        "author": "Anonymous",
        "quote": "Do not bring me your successes; they weaken me. Bring me your problems; they strengthen me."
    },
    {
        "author": "Liam Thomas Ryder",
        "quote": "Time sets the stage; fate writes the script; but only we may choose our character."
    },
    {
        "author": "Lucius Annaeus Seneca",
        "quote": "Difficulties strengthen the mind, as labor does the body."
    },
    {
        "author": "William Clement Stone",
        "quote": "Aim for the moon. If you miss, you may hit a star."
    },
    {
        "author": "Dwight Eisenhower",
        "quote": "Pull the string, and it will follow wherever you wish. Push it, and it will go nowhere at all."
    },
    {
        "author": "Benjamin Disraeli",
        "quote": "The secret of success is to be ready when your opportunity comes."
    },
    {
        "author": "Albert Einstein",
        "quote": "A person who never made a mistake never tried anything new."
    },
    {
        "author": "Calvin Coolidge",
        "quote": "Persistence and determination alone are omnipotent."
    },
    {
        "author": "Henry Ford",
        "quote": "Nothing is particularly hard if you divide it into small jobs."
    },
    {
        "author": "Dr.Seuss",
        "quote": "You have brains in your head. Your feet in your shoes. You can steer yourself in any direction you choose."
    },
    {
        "author": "Peter Drucker",
        "quote": "Whenever you see a successful business, someone once made a courageous decision."
    },
    {
        "author": "Charles Kettering",
        "quote": "My interest is in the future because I am going to spend the rest of my life there."
    },
    {
        "author": "Confucius",
        "quote": "Choose a job you love, and you will never have to work a day in your life."
    },
    {
        "author": "Mion Sonozaki",
        "quote": "Life is like a tube of toothpaste. When you've used all the toothpaste down to the last squeeze, that's when you've really lived. Live with all your might, and struggle as long as you have life."
    },
    {
        "author": "Harold S. Kushner",
        "quote": "I think of life as a good book. The further you get into it, the more it begins to make sense."
    },
    {
        "author": "Benjamin Franklin",
        "quote": "Life's tragedy is that we get old too soon and wise too late."
    },
    {
        "author": "Spartacus",
        "quote": "There are many things given to us in this life for the wrong reasons. What we do with those blessings, that is the true test of a man."
    },
    {
        "author": "Harvey Spectre",
        "quote": "Kill them with success, bury them with a smile."
    },
    {
        "author": "Ragnar",
        "quote": "Don't waste your time looking back. You're not going that way."
    },
    {
        "author": "Kenshin Himura",
        "quote": "Whatever you lose, you'll find it again. But what you throw away you'll never get back."
    },
    {
        "author": "Hitsugaya Toshiro",
        "quote": "We are all like fireworks: We climb, we shine and always go our separate ways and become further apart. But even when that time comes, let's not disappear like a firework and continue to shine… forever."
    },
    {
        "author": "Karasuma Tadaomi",
        "quote": "If something is possible, carry on as planned. Even if it isn't possible, do it anyway."
    },
    {
        "author": "Muhammad Ali",
        "quote": "Age is whatever you think it is. You are as old as you think you are."
    },
    {
        "author": "Winston Churchill",
        "quote": "Sometimes it is not good enough to do your best; you have to do what's required."
    },
    {
        "author": "Albert Camus",
        "quote": "In the midst of winter, I found there was, within me, an invincible summer."
    },
    {
        "author": "Les Brown",
        "quote": "Accept responsibility for your life. Know that it is you who will get you where you want to go, no one else."
    },
    {
        "author": "William James",
        "quote": "The greatest discovery of my generation is that a human being can alter his life by altering his attitudes."
    },
    {
        "author": "Albert Einstein",
        "quote": "If you want to live a happy life, tie it to a goal, not to people or things."
    },
    {
        "author": "J.P. Morgan",
        "quote": "The first step towards getting somewhere is to decide that you are not going to stay where you are."
    },
    {
        "author": "Henry Ford",
        "quote": "Most people spend more time and energy going around problems than in trying to solve them."
    },
    {
        "author": "Bob Brown",
        "quote": "Behind every successful man there's a lot of unsuccessful years."
    },
    {
        "author": "Nancy Simms",
        "quote": "Winners take chances. Like everyone else, they fear failing, but they refuse to let fear control them."
    },
    {
        "author": "Elmer Clark",
        "quote": "Great people are created by great mistakes that are learned from, not from great successes that are gloated upon."
    },
    {
        "author": "Charles M. Schwab",
        "quote": "The best place to succeed is where you are with what you have."
    },
    {
        "author": "Goethe",
        "quote": "The man who is born with a talent which he is meant to use finds his greatest happiness in using it."
    },
    {
        "author": "Indira Gandhi",
        "quote": "Whenever you take a step forward, you are bound to disturb something."
    },
    {
        "author": "Henry Ford",
        "quote": "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it."
    },
    {
        "author": "Henry Chester",
        "quote": "Enthusiasm is the greatest asset in the world. It beats money, power and influence."
    },
    {
        "author": "Anita DeFrantz",
        "quote": "Your goal should be out of reach but not out of sight."
    },
    {
        "author": "Marden",
        "quote": "A constant struggle, a ceaseless battle to bring success from inhospitable surroundings, is the price of all great achievements."
    },
    {
        "author": "John Wooden ",
        "quote": "Things turn out the best for the people who make the best of the way things turn out."
    },
    {
        "author": "Leo Buscaglia",
        "quote": "Your talent is God's gift to you. What you do with it is your gift back to God."
    },
    {
        "author": "Korosensei ",
        "quote": "The difference between the novice and the master is that the master has failed more times than the novice has tried."
    },
    {
        "author": "Plato",
        "quote": "Good actions give strength to ourselves and inspire good actions in others."
    },
    {
        "author": "Marcus Aurelius ",
        "quote": "The happiness of your life depends upon the quality of your thoughts; therefore guard accordingly."
    },
    {
        "author": "Bob Dole ",
        "quote": "The horizon is out there somewhere if you just keep looking for it, chasing it, and working for it."
    },
    {
        "author": "Henry Ward Beecher ",
        "quote": "Every tomorrow has two handles. We can take hold of it with the handle of anxiety or the handle of faith."
    },
    {
        "author": "Kaizaki Arata ",
        "quote": "Trying to knock others down a peg just means lowering yourself. Don't go trampling all the hardwork and trust you've built up. It insults the effort you put in."
    },
    {
        "author": "Orison Swett Marden ",
        "quote": "Go as far as you can see, and when you get there you will see further."
    },
    {
        "author": "Richard Nixon",
        "quote": "The game of life is to come up a winner, to be a success, and to achieve what you set out to do."
    },
    {
        "author": "Kaizaki Arata ",
        "quote": "You're just too busy comparing yourself to others to see. Those comparisons aren't the only measure. Don't say it's all pointless. You've worked hard and made yourself better. That's what you got in return. So don't put yourself down like this."
    },
    {
        "author": "Theodore Roosevelt ",
        "quote": "Keep your eyes on the stars and your feet on the ground."
    },
    {
        "author": "Max de Pree",
        "quote": "We cannot become what we need to be by remaining what we are."
    },
    {
        "author": "Benjamin Disraeli ",
        "quote": "One secret of success in life is for a man to be ready for his opportunity when it comes."
    },
    {
        "author": "Sugar Ray Robinson",
        "quote": "To be a champion, you have to believe in yourself when nobody else will."
    },
    {
        "author": "Henry David Thoreau",
        "quote": "I am grateful for what I am and have. My thanksgiving is perpetual."
    },
    {
        "author": "W.B. Yeats",
        "quote": "The world is full of magic things, patiently waiting for our senses to grow sharper."
    },
    {
        "author": "Thomas Edison",
        "quote": "Everything comes to him who hustles while he waits."
    },
    {
        "author": "John F. Kennedy",
        "quote": "We need men who can dream of things that never were."
    },
    {
        "author": "Carl Jung",
        "quote": "Your vision will become clear only when you can look into your own heart."
    },
    {
        "author": "Helen Keller",
        "quote": "The best and most beautiful things in the world cannot be seen or even touched. They must be felt with the heart."
    },
    {
        "author": "Leo Buscaglia",
        "quote": "Risks must be taken, because the greatest hazard in life is to risk nothing."
    },
    {
        "author": "Albert Einstein",
        "quote": "Try not to be a man of success, but a man of value."
    },
    {
        "author": "Vince Lombardi",
        "quote": "The achievements of an organisation are the results of the combined effort of each individual."
    },
    {
        "author": "Dale Carnegie",
        "quote": "Remember happiness doesn't depend upon who you are or what you have; it depends solely on what you think."
    },
    {
        "author": "Victoria Holt",
        "quote": "Never regret. If it's good, it's wonderful. If it's bad, it's experience."
    },
    {
        "author": "T. S. Elliot",
        "quote": "Only those who will risk going too far can possibly find out how far one can go."
    },
    {
        "author": "John F. Kennedy",
        "quote": "Change is the law of life and those who look only to the past or present are certain to miss the future."
    },
    {
        "author": "Thomas Jefferson",
        "quote": "I find that the harder I work, the more luck I seem to have."
    },
    {
        "author": "Hegel",
        "quote": "We may affirm absolutely that nothing great in the world has been accomplished without passion."
    },
    {
        "author": "Stew Leonard",
        "quote": "Don't go into business to get rich. Do it to enrich people. It will come back to you."
    },
    {
        "author": "Mark Twain",
        "quote": "Great things can happen when you don't care who gets the credit."
    },
    {
        "author": "Harry S Truman",
        "quote": "It is amazing what you can accomplish if you do not care who gets the credit."
    },
    {
        "author": "Arnold Glasow",
        "quote": "A good leader takes a little more than his share of the blame, a little less than his share of the credit."
    },
    {
        "author": "Plato",
        "quote": "Never discourage anyone who continually makes progress, no matter how slow."
    },
    {
        "author": "Brian Tracy",
        "quote": "A clear vision, backed by definite plans, gives you a tremendous  feeling of confidence and personal power."
    },
    {
        "author": "Michael Jordan",
        "quote": "Some people want it to happen, some wish it would happen, others make it happen."
    },
    {
        "author": "Denis Waitley",
        "quote": "Goals are like stepping- stones to the stars. They should never be used to put a ceiling or a limit on achievement."
    },
    {
        "author": "Winston Churchill",
        "quote": "A lie gets halfway around the world before the truth has a chance to get its pants on."
    },
    {
        "author": "William James",
        "quote": "The greatest discovery of my generation is that human beings can alter their lives by altering their attitudes of mind."
    },
    {
        "author": "Napoleon Hill",
        "quote": "Every adversity, every failure, every heartache carries with it the seed on an equal or greater benefit."
    },
    {
        "author": "Aristotle",
        "quote": "Where your talents and the needs of the world cross lies your calling."
    },
    {
        "author": "Maya Angelou",
        "quote": "Life is not measured by the number of breaths we take, but by the moments that take our breath away."
    },
    {
        "author": "Nelson Mandela",
        "quote": "A good head and a good heart are always a formidable combination."
    },
    {
        "author": "Mario Andretti",
        "quote": "If everything seems under control, you're just not going fast enough."
    },
    {
        "author": "Jim Watkins",
        "quote": "A river cuts through rock, not because of its power, but because of its persistence."
    },
    {
        "author": "Voltaire",
        "quote": "The longer we dwell on our misfortunes the greater is their power to harm us."
    },
    {
        "author": "Dale Carnegie",
        "quote": "Remember happiness doesn't depend upon who you are or what you have; it depends solely on what you think."
    },
    {
        "author": "Mother Teresa",
        "quote": "Be faithful in small things because it is in them that your strength lies."
    },
    {
        "author": "Thomas Edison",
        "quote": "I am not discouraged, because every wrong attempt discarded is another step forward."
    },
    {
        "author": "Nelson Mandela",
        "quote": "A good head and a good heart are always a formidable combination."
    },
    {
        "author": "John F. Kennedy",
        "quote": "Change is the law of life and those who look only to the past or present are certain to miss the future."
    },
    {
        "author": "Diane Sawyer",
        "quote": "Whatever you want in life, other people are going to want it too. Believe in yourself enough to accept the idea that you have an equal right to it."
    },
    {
        "author": "Peter Drucker",
        "quote": "The greatest danger in times of turbulence is not the turbulence; it is to act with yesterday's logic."
    },
    {
        "author": "Ralph Blum",
        "quote": "Nothing is predestined: The obstacles of your past can become the gateways that lead to  new beginnings."
    },
    {
        "author": "Don Zimmer",
        "quote": "What you lack in talent can be made up with desire, hustle and giving 110 percent all the time."
    },
    {
        "author": "Cherie Carter-Scott",
        "quote": "Remember, there are no mistakes, only lessons. Love yourself, trust your choices, and everything is possible."
    },
    {
        "author": "Bill Parcells",
        "quote": "A team divided against itself can break down at any moment. The least bit of pressure or adversity will crack it apart."
    },
    {
        "author": "Doug Collins",
        "quote": "Anytime you are trying to bring out the best in someone, there is going to be creative tension."
    },
    {
        "author": "Lou Holtz",
        "quote": "Don't ever ask a player to do something he doesn't have the ability to do. He'll just question your ability as a coach, not his as an athlete."
    },
    {
        "author": "Jim Rohn",
        "quote": "If you are not willing to risk the usual you will have to settle for the ordinary."
    },
    {
        "author": "Liane Cardes ",
        "quote": "Continuous effort, not strength or intelligence is the key to unlocking our potential."
    },
    {
        "author": "Benjamin Franklin ",
        "quote": "Those who love deeply never grow old; they may die of old age, but they die young."
    },
    {
        "author": "Albert Camus",
        "quote": "Those who lack the courage will always find a philosophy to justify it."
    },
    {
        "author": "Thomas Szasz",
        "quote": "When a person can no longer laugh at himself, it is time for others to laugh at him."
    },
    {
        "author": "Steve Jobs",
        "quote": "You have to trust in something-   your gut, destiny, life, karma, whatever. This approach has never let me down, and it has made all the difference in my life."
    },
    {
        "author": "Michael Altshuler",
        "quote": "The bad news is time flies. The good news is you're the pilot."
    },
    {
        "author": "Aristotle",
        "quote": "The worst form of inequality is to try to make unequal things equal."
    },
    {
        "author": "Benjamin Franklin",
        "quote": "Beware of little expenses. A small leak will sink a great ship."
    },
    {
        "author": "Stephen Hawking",
        "quote": "People won't have time for you if you are always angry or complaining."
    },
    {
        "author": "Desmond Tutu",
        "quote": "Hope is being able to see that there is light despite all of the darkness."
    },
    {
        "author": "Maria Robinson",
        "quote": "Nobody can go back and start a new beginning, but anyone can start today and make a new ending."
    },
    {
        "author": "Michael Jordon",
        "quote": "To be successful you have to be selfish, or else you never achieve. And once you get to your highest level, then you have to be unselfish. Stay reachable. Stay in touch. Don't isolate."
    },
    {
        "author": "Wayne Dyer",
        "quote": "Be miserable. Or motivate yourself. Whatever has to be done, it's always your choice."
    },
    {
        "author": "Ralph Waldo Emerson",
        "quote": "The only person you are destined to become is the person you decide to be"
    },
    {
        "author": "Joel Osteen",
        "quote": "Sometimes you face difficulties not because you're doing something wrong, but because you're doing something right."
    },
    {
        "author": "Paulo Coelho",
        "quote": "If you have a dream, don't waste your energies explaining why."
    },
    {
        "author": "Stephen Hawking",
        "quote": "I have noticed even people who claim everything is predestined, and that we can do nothing to change it, look before they cross the road."
    },
    {
        "author": "Abdul Kalam",
        "quote": "Thinking should become your capital asset, no matter whatever ups and downs you come across in your life."
    },
    {
        "author": "Mohandas Karamchand Gandhi",
        "quote": "Generosity consists not the sum given, but the manner in which it is bestowed."
    },
    {
        "author": "John C. Maxwell",
        "quote": "People may hear your words, but they feel your attitude."
    },
    {
        "author": "Malcolm X",
        "quote": "The future belongs to those who prepare for it today."
    },
    {
        "author": "Dalai Lama",
        "quote": "In order to carry a positive action we must develop here a positive vision."
    },
    {
        "author": "Henry Ford",
        "quote": "Coming together is a beginning; keeping together is progress; working together is success."
    },
    {
        "author": "Winston Churchill",
        "quote": "Success is not final, failure is not fatal: it is the courage to continue that counts."
    },
    {
        "author": "H. Jackson Brown Jr.",
        "quote": "Love is when the other person's happiness is more important than your own."
    },
    {
        "author": "Post Malone",
        "quote": "Your growth scares people who don't want to change."
    },
    {
        "author": "Michael Jordan ",
        "quote": "I can accept failure, everyone fails at something. But I can't accept not trying."
    },
    {
        "author": "Steve Jobs",
        "quote": "Quality is much better than quantity. One home run is much better than two doubles."
    },
    {
        "author": "Benjamin Franklin ",
        "quote": "Those who love deeply never grow old; they may die of old age, but they die young."
    },
    {
        "author": "Lebron James",
        "quote": "You can't be afraid to fail. It's the only way you succeed-   you're not gonna succeed all the time, and I know that."
    },
    {
        "author": "Bill Bradley",
        "quote": "Ambition is the path to success. Persistence is the vehicle you arrive in."
    },
    {
        "author": "Stephen Hawking",
        "quote": "People won't have time for you if you are always angry or complaining."
    },
    {
        "author": "Dwayne Johnson",
        "quote": "Don't be afraid to be ambitious about your goals. Hard work never stops. Neither should your dreams."
    },
    {
        "author": "Will Smith",
        "quote": "If you're absent during my struggle, don't expect to be present during my success."
    },
    {
        "author": "Celica Arfonia",
        "quote": "The one's who accomplish true greatness, are the foolish who keep pressing onward. The ones who accomplish nothing, are the wise who know when to quit."
    },
    {
        "author": "Glenn Radars",
        "quote": "Just walk the path you believe in, and don't forget you're the main character of your own life."
    },
    {
        "author": "Faraaz Kazi",
        "quote": "Some people are going to leave, but that's not the end of your story. That's the end of their part in your story."
    },
    {
        "author": "Mufti Menk",
        "quote": "Privacy is key; that is if you value your peace and mental health. Over sharing is the root of many problems. Keep it low- key. Keep it unpredictable. No drama. It's a huge barrier against those who want to destroy your plans."
    },
    {
        "author": "Albert Einstein",
        "quote": "If you are out to describe the truth, leave elegance to the tailor."
    },
    {
        "author": "Johnny Depp",
        "quote": "One day, the people that didn't believe in you will tell everyone how they met you."
    },
    {
        "author": "Malcolm X",
        "quote": "Education is our passport to the future, for tomorrow belongs to the people who prepare for it today."
    },
    {
        "author": "Kikyō (Inuyasha)",
        "quote": "The future is not a straight line. There are many different pathways. We must try to decide the future for ourselves."
    },
    {
        "author": "Malcolm X",
        "quote": "The media's the most powerful entity on earth. They have the power to make the innocent guilty and to make the guilty innocent, and that's power. Because they control the minds of the masses."
    },
    {
        "author": "Soren Kierkegaard",
        "quote": "Life can only be understood backwards; but it must be lived forwards."
    },
    {
        "author": "Saitama",
        "quote": "All our dreams can come true, if we have the courage to pursue them."
    },
    {
        "author": "Mahendra Singh Dhoni",
        "quote": "Successful people are not gifted; they just work hard then succeed on purpose."
    },
    {
        "author": "Mozzie (White Collar)",
        "quote": "If you want a happy ending, that depends, of course, on where you stop your story."
    },
    {
        "author": "Mozzie (White Collar)",
        "quote": "Realists don't fear the results of their study."
    },
    {
        "author": "Michael Jordon",
        "quote": "Obstacles don't have to stop you. If you run into a wall, don't turn around and give up. Figure out how to climb it, go through it, or work around it."
    },
    {
        "author": "Eminem (Marshall Bruce Mathers III)",
        "quote": "You can make something of your life. It just depends on your drive."
    },
    {
        "author": "Roger Federer",
        "quote": "There's no way around hard work. Embrace it."
    },
    {
        "author": "Michael Scofield",
        "quote": "I believe in being part of the solution, not the problem. Be the change you want to see in the world."
    },
    {
        "author": "Sachin Ramesh Tendulkar",
        "quote": "People throw stones at you and you convert them into milestones."
    },
    {
        "author": "Theodore Bagwell",
        "quote": "We are captives of our own identities, living in prisons of our own creation."
    },
    {
        "author": "Walter White",
        "quote": "Electrons—they change their energy levels. Molecules change their bonds. Elements—they combine and change into compounds. Well, that's all of life, right? It's the constant. It's the cycle. It's solution, dissolution, just over and over and over. It is growth, then decay, then transformation."
    },
    {
        "author": "Mike Milligan",
        "quote": "In astronomy the word 'revolution' means a celestial object that comes full circle. It's funny because on Earth it means change."
    },
    {
        "author": "Mozzie (White Collar)",
        "quote": "We can't change the direction of the wind, but we can adjust the sails."
    },
    {
        "author": "Walter White",
        "quote": "You need to stop focusing on the darkness behind you. The past is the past. Nothing can change what we've done."
    },
    {
        "author": "Shinichi Chiaki",
        "quote": "You can't sit around envying other people's worlds. You have to go out and change your own."
    },
    {
        "author": "Mugen",
        "quote": "Don't live your life making up excuses. The one making your choices is yourself!"
    },
    {
        "author": "Riza Hawkeye",
        "quote": "The heroes during times of war are nothing but mass murderers during times of peace."
    },
    {
        "author": "Uchiha Madara",
        "quote": "Power is not will, it is the phenomenon of physically making things happen."
    },
    {
        "author": "Yuki Takeya",
        "quote": "There are days when nothing goes right. There are days when you stumble and fall. There are days when you just want to cry. To cry a lot. To sleep a lot. Or even eat a lot. It's alright, as long as you pick yourself up again."
    },
    {
        "author": "Zig Ziglar",
        "quote": "Lack of direction, not lack of time, is the problem. We all have twenty- four hour days."
    },
    {
        "author": "Albert Einstein",
        "quote": "Life is like riding a bicycle. To keep your balance, you must keep moving."
    },
    {
        "author": "Ai Yazawa",
        "quote": "The things that stress me out haven't changed."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Do not fear failure but rather fear not trying."
    },
    {
        "author": "Markus Zusak",
        "quote": "Sometimes people are beautiful."
    },
    {
        "author": "Riza Hawkeye",
        "quote": "War does not determine who is right — only who is left."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Never lose hope. Storms make people stronger and never last forever."
    },
    {
        "author": "Woody Allen",
        "quote": "I'm not afraid of death; I just don't want to be there when it happens."
    },
    {
        "author": "Gildarts Clive",
        "quote": "Fear is not evil. It tells you what your weakness is. And once you know your weakness, you can become stronger, as well as kinder."
    },
    {
        "author": "Steve Maraboli",
        "quote": "Letting go means to come to the realization that some people are a part of your history, but not a part of your destiny."
    },
    {
        "author": "Dr. Seuss",
        "quote": "Today you are You, that is truer than true. There is no one alive who is Youer than You."
    },
    {
        "author": "Uchiha Obito",
        "quote": "In the world, those who break the rules are scum, but those who abandon their friends are worse than scum."
    },
    {
        "author": "Viktor E. Frankl",
        "quote": "Everything can be taken from a man but one thing: the last of the human freedoms—to choose one's attitude in any given set of circumstances, to choose one's own way."
    },
    {
        "author": "George Bernard Shaw",
        "quote": "Life isn't about finding yourself. Life is about creating yourself."
    },
    {
        "author": "Jiraiya",
        "quote": "A person grows up when he's able to overcome hardships. Protection is important, but there are some things that a person must learn on his own."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Be brave to stand for what you believe in even if you stand alone."
    },
    {
        "author": "Dr. Seuss",
        "quote": "Sometimes the questions are complicated and the answers are simple."
    },
    {
        "author": "Monkey D.Luffy",
        "quote": "No matter how hard or impossible it is, never lose sight of your goal."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Life is about accepting the challenges along the way, choosing to keep moving forward, and savoring the journey."
    },
    {
        "author": "Pablo Picasso",
        "quote": "Everything you can imagine is real."
    },
    {
        "author": "Tite Kubo",
        "quote": "Whats the difference between a king and his horse?I don't mean some kiddy shit like one has 4 legs and the other has 2, or ones a person and ones an animal. If their form, ability, and power is exactly the same, then why is it one becomes the king and controls the battle and the other one becomes the horse and carries the king? There's only one answer...INSTINCT!!!"
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Be grateful for what you already have while you pursue your goals."
    },
    {
        "author": "Marilyn Monroe",
        "quote": "This life is what you make it. No matter what, you're going to mess up sometimes, it's a universal truth. But the good part is you get to decide how you're going to mess it up. Girls will be your friends-   they'll act like it anyway. But just remember, some come, some go. The ones that stay with you through everything-   they're your true best friends. Don't let go of them. Also remember, sisters make the best friends in the world. As for lovers, well, they'll come and go too. And baby, I hate to say it, most of them-   actually pretty much all of them are going to break your heart, but you can't give up because if you give up, you'll never find your soulmate. You'll never find that half who makes you whole and that goes for everything. Just because you fail once, doesn't mean you're gonna fail at everything. Keep trying, hold on, and always, always, always believe in yourself, because if you don't, then who will, sweetie? So keep your head high, keep your chin up, and most importantly, keep smiling, because life's a beautiful thing and there's so much to smile about."
    },
    {
        "author": "Tsugumi Ohba",
        "quote": "There are going to be times when you learn more about the world you're entering and feel defeated when you see the gap between the ideal and the reality… But that's something we'll all face. The people that face those obstacles and overcome them are people whose dreams come true."
    },
    {
        "author": "William James",
        "quote": "Action may not always bring happiness, but there is no happiness without action."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Start each day with a positive thought and a grateful heart."
    },
    {
        "author": "Douglas Adams",
        "quote": "I may not have gone where I intended to go, but I think I have ended up where I needed to be."
    },
    {
        "author": "Neil Armstrong",
        "quote": "I believe every human has a finite number of heartbeats. I don't intend to waste any of mine."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Pursue what catches your heart, not what catches your eyes."
    },
    {
        "author": "Allen Saunders",
        "quote": "Life is what happens to us while we are making other plans."
    },
    {
        "author": "Natsuki Takaya",
        "quote": "Just be yourself and you'll be fine."
    },
    {
        "author": "Aisha Tyler",
        "quote": "Nothing really worth having is easy to get. The hard- fought battles, the goals won with sacrifice, are the ones that matter."
    },
    {
        "author": "Mark Twain",
        "quote": "Good friends, good books, and a sleepy conscience: this is the ideal life."
    },
    {
        "author": "Stanley Sugerman (Hustle)",
        "quote": "You got to be an iceberg out there, all floating around, and sharp, and taking down ships."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Success is not how high you have climbed, but how you make a positive difference to the world."
    },
    {
        "author": "J.K. Rowling",
        "quote": "It does not do to dwell on dreams and forget to live."
    },
    {
        "author": "Ai Yazawa",
        "quote": "People are only what they think of themselves."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Do what is right, not what is easy nor what is popular."
    },
    {
        "author": "Albert Einstein",
        "quote": "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle."
    },
    {
        "author": "Steve Maraboli",
        "quote": "Sometimes life knocks you on your ass... get up, get up, get up!!! Happiness is not the absence of problems, it's the ability to deal with them."
    },
    {
        "author": "Steve Maraboli",
        "quote": "The truth is, unless you let go, unless you forgive yourself, unless you forgive the situation, unless you realize that the situation is over, you cannot move forward."
    },
    {
        "author": "Andre Gide",
        "quote": "It is better to be hated for what you are than to be loved for what you are not."
    },
    {
        "author": "Ai Yazawa",
        "quote": "In this world, not everything will be won by justice. If you want to win, you have to learn how to cheat. (Nana)"
    },
    {
        "author": "Roy T. Bennett",
        "quote": "It's only after you've stepped outside your comfort zone that you begin to change, grow, and transform."
    },
    {
        "author": "Narcotics Anonymous",
        "quote": "Insanity is doing the same thing, over and over again, but expecting different results."
    },
    {
        "author": "Wayne Gretzky",
        "quote": "You miss 100% of the shots you don't take."
    },
    {
        "author": "Kobe Bryant",
        "quote": "The harder you work, the luckier you get."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine."
    },
    {
        "author": "Oscar Wilde",
        "quote": "To live is the rarest thing in the world. Most people exist, that is all."
    },
    {
        "author": "Hiromu Arakawa",
        "quote": "Even when our eyes are closed, there's a whole world that exists outside ourselves and our dreams."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Live the Life of Your Dreams: Be brave enough to live the life of your dreams according to your vision and purpose instead of the expectations and opinions of others."
    },
    {
        "author": "Robert Frost",
        "quote": "In three words I can sum up everything I've learned about life: it goes on."
    },
    {
        "author": "Stanley Sugerman (Hustle)",
        "quote": "It's good to be nervous. It means you give a shit."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart."
    },
    {
        "author": "Mae West",
        "quote": "You only live once, but if you do it right, once is enough."
    },
    {
        "author": "Stanley Sugerman (Hustle)",
        "quote": "Obsession is going to beat talent every time."
    },
    {
        "author": "Roy T. Bennett",
        "quote": "Attitude is a choice. Happiness is a choice. Optimism is a choice. Kindness is a choice. Giving is a choice. Respect is a choice. Whatever choice you make makes you. Choose wisely."
    },
    {
        "author": "William W. Purkey",
        "quote": "You've gotta dance like there's nobody watching."
    },
    {
        "author": "Uchiha Madara",
        "quote": "When a man learns to love, he must bear the risk of hatred."
    },
    {
        "author": "Frank Herbert",
        "quote": "I must not fear. Fear is the mind- killer. Fear is the little- death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain."
    },
    {
        "author": "Marilyn Monroe",
        "quote": "I'm selfish, impatient and a little insecure. I make mistakes, I am out of control and at times hard to handle. But if you can't handle me at my worst, then you sure as hell don't deserve me at my best."
    },
    {
        "author": "Pseudonymous Bosch",
        "quote": "Books can also provoke emotions. And emotions sometimes are even more troublesome than ideas. Emotions have led people to do all sorts of things they later regret- like, oh, throwing a book at someone else."
    }
]


def main():
    custom_font_path = "Poppins-Medium.ttf"
    for idx, x in enumerate(quotesArray):
        video_output_path = os.path.join(output_dir, f"video_{idx}.mp4")
        if os.path.exists(video_output_path):
            print(f"Skipping quote {idx} as it already exists")
            continue
        else:
            author = x["author"]
            quote = x["quote"]
            print(f"Processing quote {idx}: {quote}")
            random_audio = "natureaudio/" + random.choice(mp3files)
            audio_path = random_audio

            # Choose a random background video
            bg_video_path = "naturevideo/" + random.choice(mp4files)

            # Load the background video and get its duration
            bg_video_clip = VideoFileClip(bg_video_path)
            bg_video_duration = 20.0  # Set to 20 seconds

            # Load the audio clip
            audio_clip = AudioFileClip(audio_path)

            # Create video clip with background video and audio
            video_clip = VideoFileClip(
                bg_video_path).subclip(0, bg_video_duration)
            video_clip = video_clip.set_audio(audio_clip)

            # Set video duration to 20 seconds
            video_clip = video_clip.subclip(0, bg_video_duration)
            # insert the line break in every 30 characters
            max_line_length = 35
            wrapped_text = wrap_text(quote, max_line_length)
            txt = TextClip(
                txt=wrapped_text + "\n\n" + author,
                fontsize=26,
                color="white",
                font=custom_font_path,
            )

            padding = 30
            txt_clip = txt.margin(
                top=padding, bottom=padding, left=padding, right=padding, opacity=0)

            # Create a solid color background for the text
            txt_bg = ColorClip(size=txt_clip.size, color=random.choice(color))

            # Overlay the TextClip on the background
            txt_clip = CompositeVideoClip([txt_bg.set_duration(bg_video_duration), txt_clip.set_duration(
                bg_video_duration).set_position(("center", "center"))])

            # Overlay the TextClip on the video
            video_with_text = CompositeVideoClip([video_clip.set_duration(
                bg_video_duration), txt_clip.set_duration(bg_video_duration).set_position(("center", "center"))])

            # Create output video file

            video_with_text.write_videofile(
                video_output_path, codec="libx264", audio_codec="aac")


main()
