import os
import datetime
from beem import Steem
from beem.comment import Comment

# ==========================================
# 1. CONFIGURATION VARIABLES
# ==========================================
MY_ACCOUNT = "bnwt"  
TARGET_COMMUNITY = "hive-129948"  
CUSTOM_TAGS = ["amarbanglablog", "art", "meme", "trc-20", "sunpump", "puss", "krsuccess"]

# ========================================================
# 2. The specific account receiving 100% of the rewards
# ========================================================
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"  # Your worker endpoint

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)
    
# ===============================================
# 3. 32-Day Rotated Content Library (English)
# ===============================================
ARTICLES_POOL = {
    1: {
        "title": "Embracing Fresh Beginnings and New Opportunities",
        "image": "https://cdn.steemitimages.com/DQmaoTkXWbJoxqQvGZLd4BSF1rmbSsqWUNhspxXoH9SSM6S/1000022690.jpg",
        "body": "Every single sunrise brings a silent invitation to reset our goals and leave past setbacks behind. It is easy to get caught up in yesterday's mistakes, but true growth happens when we focus entirely on the present moment.\n\nTake a few minutes today to list three small things you want to achieve. By breaking down your broader ambitions into daily, actionable steps, you build a sustainable momentum that naturally propels you forward."
    },
    2: {
        "title": "The Power of Intentional Daily Micro-Habits",
        "image": "https://cdn.steemitimages.com/DQmaLnDaUxmzXGKAuTNtULkYUE9aad5LnPPvLffSJB9F82N/1000022691.jpg",
        "body": "We often underestimate the massive impact that tiny, daily choices have on our long-term success. Reading just five pages of a book or stretching for ten minutes might feel insignificant in the moment, but consistency multiplies these actions over time.\n\nExamine your current morning routine and see where you can slip in one healthy micro-habit. Commit to practicing it without fail today, and watch how it subtly shifts your energy and focus."
    },
    3: {
        "title": "Cultivating Mindful Awareness in a Busy World",
        "image": "https://cdn.steemitimages.com/DQmWtziQ9RGQLpmZPtb8mU6GEZCwABe6x2idCZFxaAkCVoZ/1000022692.jpg",
        "body": "Modern life constantly pulls our attention in a thousand directions, leaving us feeling scattered and drained. Cultivating mindfulness doesn't mean sitting in silence for hours; it simply means being fully anchored where your feet are right now.\n\nTry to eat your next meal or drink your coffee without looking at a digital screen. Pay attention to the textures, temperatures, and tastes, allowing your nervous system a much-needed moment to rest and recalibrate."
    },
    4: {
        "title": "Finding Deep Creative Inspiration in Quiet Spaces",
        "image": "https://cdn.steemitimages.com/DQmNPUz7L3GwkpnCrpRz5Vddkt9fuLdF6iSyoU9YpLF2qvT/1000022693.jpg",
        "body": "Inspiration rarely strikes when our minds are cluttered with notifications, chores, and endless digital noise. True creative breakthroughs usually happen during the quiet, unstructured gaps of our day when thoughts are free to wander.\n\nStep away from your desk today and take a short walk without your headphones or phone. Let your surroundings fill your senses naturally, and you might be surprised by the fresh ideas that bubble to the surface."
    },
    5: {
        "title": "The Crucial Balance Between Hard Work and Rest",
        "image": "https://cdn.steemitimages.com/DQmeSRJNKRgct5GePYCZugKeN2wdsV6bv5rP9ePGQ3UUojh/1000022694.jpg",
        "body": "Society heavily glorifies the constant hustle, but chronic exhaustion is never a sustainable strategy for true success. Rest is not a reward you have to earn after collapsing; it is a fundamental requirement for peak performance.\n\nTreat your downtime with the exact same respect you give to your most important professional business meetings. Schedule an hour this evening purely for relaxation, ensuring your mind and body can genuinely recover."
    },
    6: {
        "title": "Nurturing Professional Growth Through Active Learning",
        "image": "https://cdn.steemitimages.com/DQmSzQKFVTCXgYyjPMkZWCqPgiFmVP9b2p1pyrjregP6x4T/1000022695.jpg",
        "body": "The landscape of work and technology changes so rapidly that stagnant skills quickly become obsolete. Dedicating yourself to lifelong learning is the absolute best insurance policy for your future career and personal development.\n\nFind a short educational article, podcast episode, or tutorial video related to your field today. Invest just fifteen minutes into absorbing that content and consider how you can apply it directly to your current projects."
    },
    7: {
        "title": "Building Resilience Against Life's Unexpected Hurdles",
        "image": "https://cdn.steemitimages.com/DQmVbdHEfirRrNHiNUeeYJ9ZRAizpecDhSrKWgNfWxERso9/1000022696.jpg",
        "body": "Challenges and disruptions are completely unavoidable, but our emotional response to them remains entirely under our control. Developing resilience isn't about ignoring hardships; it is about learning how to adapt and bounce back faster.\n\nWhen a minor frustration happens today, pause and ask yourself if this issue will matter in five weeks. Shifting your timeline perspective instantly dilutes stress and helps you approach problem-solving with a calm, clear mind."
    },
    8: {
        "title": "The Overlooked Value of Practicing Active Listening",
        "image": "https://cdn.steemitimages.com/DQmUm4SPqzsFnJFqxUcyfLWcpBshc5WwRctaELwq5sxFnx4/1000022697.jpg",
        "body": "Most people do not listen with the intent to understand; they listen solely with the intent to reply. True connection and deep collaboration happen when we quiet our inner monologues and completely focus on the speaker's words.\n\nIn your conversations today, challenge yourself to let the other person finish their thoughts entirely before you speak. Ask thoughtful follow-up questions instead of immediately shifting the topic back to your own experiences."
    },
    9: {
        "title": "Decluttering Your Digital Environment for Mental Clarity",
        "image": "https://cdn.steemitimages.com/DQmTSUK72sd8y7xdyzjjvX89B5xsonqsayJsAmU8yi3wtz4/1000022699.jpg",
        "body": "A messy digital workspace can cause just as much subconscious anxiety and distraction as a cluttered physical desk. Overflowing email inboxes, unorganized desktop files, and useless notifications constantly fragment our cognitive focus.\n\nSpend ten minutes today unsubscribing from newsletters you no longer read and deleting old files. A streamlined digital environment creates an immediate sense of mental clarity and makes your daily workflow much smoother."
    },
    10: {
        "title": "Unlocking Potential Through Genuine Self-Compassion",
        "image": "https://steemitimages.com",
        "body": "We are frequently our own harshest critics, speaking to ourselves in ways we would never dream of speaking to a friend. While self-criticism feels like motivation, it actually triggers stress and hinders long-term personal growth.\n\nIf you make a mistake today, consciously replace harsh self-blame with understanding and constructive analysis. Acknowledge that errors are simply data points on the path toward mastering any new skill or lifestyle habit."
    },
    11: {
        "title": "The Subtle Art of Protecting Your Personal Energy",
        "image": "https://cdn.steemitimages.com/DQme7XoodSLN2Z9mKgh72U6S9wbg2RWQSAqvtmieJECjuhS/1000022700.jpg",
        "body": "Your time and emotional energy are finite resources that must be managed with great care every day. Saying yes to every single request or absorbing other people's chronic negativity leaves you with nothing left for yourself.\n\nPractice setting polite but firm boundaries today regarding your schedule and mental availability. Protecting your personal peace ensures that you can bring your best, most authentic self to the things that truly matter."
    },
    12: {
        "title": "Finding Deep Fulfillment in Simple Daily Pleasures",
        "image": "https://cdn.steemitimages.com/DQmbqHXa2687McMdkSZQwsc8HmJwqrko4mLddUdaEkvL2py/1000022702.jpg",
        "body": "It is incredibly easy to spend our lives waiting for monumental milestones to finally feel happy and content. However, true life satisfaction is actually built from noticing and savoring minor, everyday moments of joy.\n\nWhether it is the warmth of morning sunlight, a great cup of tea, or a pleasant laugh with a coworker, lean into it. Pause for ten seconds to fully appreciate these simple pleasures as they happen throughout your afternoon."
    },
    13: {
        "title": "Overcoming Procrastination by Simplifying the First Step",
        "image": "https://cdn.steemitimages.com/DQmPwyNkp8Ya6hUwK2dnWSx9VuTr5QQn5PGMGLHRC29BdcV/1000022704.jpg",
        "body": "Procrastination is rarely caused by laziness; it is usually an emotional coping mechanism for a task that feels overwhelming. When a project seems too massive, our brains naturally look for immediate distractions to avoid the discomfort.\n\nTricked by size, break your toughest task today down into a step so ridiculously small that it requires almost zero effort. Commit to working on just that single micro-step for five minutes, and let the initial friction dissolve."
    },
    14: {
        "title": "Curating Your Mind's Daily Information Diet",
        "image": "https://cdn.steemitimages.com/DQmTSffmCd9weEvEKxxKUzWFHKhoH38B8FeTefjxrTbmTsT/1000022705.jpg",
        "body": "Just like the food we eat shapes our physical health, the media we consume shapes our psychological well-being. Consistently consuming sensationalized news and toxic social feeds creates a skewed, anxious outlook on reality.\n\nTake an honest inventory of the accounts and websites you visit most frequently throughout the week. Replace at least one negative source with educational content, inspiring essays, or community-focused platforms."
    },
    15: {
        "title": "The Ripple Effect of Small Acts of Kindness",
        "image": "https://cdn.steemitimages.com/DQmcCqZV7g9JUFRWRdb55UycbaHppxx4xfzoZRvnkWrsbPz/1000022708.jpg",
        "body": "We often think we need to make grand, expensive gestures to positively impact the lives of the people around us. In reality, a genuine compliment, an open door, or a supportive text message can completely turn someone's day around.\n\nMake it a goal to deliver one unexpected expression of kindness or appreciation to someone today. These small actions create a beautiful ripple effect, lifting both the recipient's spirits and your own emotional state."
    },
    16: {
        "title": "The Power of Defining Clear Financial Goals",
        "image": "https://cdn.steemitimages.com/DQmUzhBJBrxyYxqV71UHQsXSvPAP7vVToKCJHpn9TgKWjqd/1000022709.jpg",
        "body": "Vague desires like 'wanting to save money' rarely lead to lasting behavioral changes. True financial empowerment begins when you define exact, measurable targets—such as building a specific three-month emergency fund or outlining a clear debt repayment timeline.\n\nTake fifteen minutes today to write down one concrete financial milestone for the upcoming year. Breaking this target down into precise monthly or weekly contributions transforms an intimidating mountain into a clear, manageable roadmap."
    },
    17: {
        "title": "Embracing the Uncomfortable Journey of Personal Growth",
        "image": "https://cdn.steemitimages.com/DQmaR5iWD561aK73j45LhwiLRmJY98ahAc6gP34viadLC3u/1000022710.jpg",
        "body": "Real personal growth never happens inside the cozy, familiar boundaries of our comfort zones. True progress requires us to step out into the awkward, uncertain spaces where failure and learning coexist.\n\nChoose one task or conversation you have been actively avoiding because it feels slightly uncomfortable or intimidating. Confront it directly today, knowing that enduring temporary discomfort is how you expand your personal capabilities."
    },
    18: {
        "title": "How Physical Movement Boosts Daily Brain Power",
        "image": "https://cdn.steemitimages.com/DQmTUzNxhgViGn4kpP3pSHdAM2e8XmAvqjwtKDfZ9hVD8AQ/1000022711.jpg",
        "body": "Our bodies and minds are deeply interconnected systems that constantly influence one another's performance. Sitting motionless at a desk for long stretches reduces blood flow to the brain, causing sluggish thinking and fatigue.\n\nBreak up your sedentary blocks today by standing up to stretch or walking around every single hour. Even two minutes of light physical movement re-oxygenates your system, instantly boosting your focus, mood, and productivity."
    },
    19: {
        "title": "Shifting Focus From Final Outcomes to Daily Systems",
        "image": "https://cdn.steemitimages.com/DQmaL2iSSenuKZkWHrWhrh78ZvxGPhXqCqEHo2QLzZyFf2i/1000022712.jpg",
        "body": "Fixating purely on a distant goal can leave you feeling discouraged by how far you still have left to go. Winners and losers often share the exact same goals; it is the daily system execution that separates them.\n\nForget about the ultimate endpoint for a moment and focus entirely on executing your routine perfectly today. Trust that if your daily systems are solid, the desired results will naturally take care of themselves over time."
    },
    20: {
        "title": "The Life-Changing Magic of Keeping a Workspace Clean",
        "image": "https://cdn.steemitimages.com/DQmRhWtNiV58rnU2z1CbsU5M4T8Y2563FS4kRsJidALpJrF/1000022713.jpg",
        "body": "A physical environment filled with scattered papers, empty cups, and random objects creates subtle, constant mental friction. It forces your brain to expend energy filtering out visual distractions, lowering your overall working memory capacity.\n\nBefore you start your primary tasks today, clear everything off your desk except for the absolute essentials. You will immediately notice a lighter mental load and an increased ability to lock into your deep work blocks."
    },
    21: {
        "title": "Cultivating Patience in an Era of Instant Gratification",
        "image": "https://cdn.steemitimages.com/DQmcM8idjKHLcGrQvDDHYZGhqfd3DJcE8cuP7bgLaMLE6Vn/1000022714.jpg",
        "body": "We live in an on-demand world where fast delivery, instant streams, and quick replies have warped our expectations. Because we get minor things instantly, we mistakenly expect major life transformations to happen overnight as well.\n\nRemind yourself today that worthwhile things like career mastery, deep relationships, and physical fitness require time. Embrace the slow, steady process and practice patience when things don't yield immediate results."
    },
    22: {
        "title": "The Strategic Value of Conducting Regular Self-Reviews",
        "image": "https://cdn.steemitimages.com/DQmUf7cBsP3N1VUuUcyXosroc8K8syAeUTo4LpMEkuNf4U2/1000022715.jpg",
        "body": "It is incredibly easy to stay endlessly busy while inadvertently moving in completely the wrong direction. Without regular periods of self-reflection, we repeat ineffective habits and lose track of our core priorities.\n\nSet aside a brief window at the end of this week to review what went well and what felt draining. Use these insights to make small adjustments to your schedule, ensuring your daily actions stay aligned with your values."
    },
    23: {
        "title": "Learning to Say No with Ultimate Confidence and Grace",
        "image": "https://cdn.steemitimages.com/DQmcmchob83PY1kU8aSJhLVWHPLJuQP2v9uCA38UAy5NZ1N/1000022716.jpg",
        "body": "Every time you say yes to a non-essential request, you are automatically saying no to your own top priorities. People-pleasing might feel kind in the moment, but it ultimately leads to resentment and severe personal burnout.\n\nWhen someone asks for your time today, check your true capacity before giving an answer. It is entirely acceptable to deliver a polite, honest refusal in order to preserve your focus for your core commitments."
    },
    24: {
        "title": "Unlocking Creative Solutions Through Critical Thinking",
        "image": "https://cdn.steemitimages.com/DQmNuCAKJtopL4cXK8FRvrxQKBwVawxFfXKG9htdY6o4oNK/1000022717.jpg",
        "body": "When faced with an unexpected obstacle, our default response is often to panic or rely on outdated habits. Critical thinking involves stepping back, challenging assumptions, and looking at the core problem from entirely new angles.\n\nIf you hit a roadblock today, don't just force your way through using the same old tired methods. Ask yourself how an outsider would solve this, and look for a more efficient, elegant workaround."
    },
    25: {
        "title": "Developing a Grounded Perspective on Perfectionism",
        "image": "https://cdn.steemitimages.com/DQmTyjc2tER6G3KqWeF5PJiQnwubkTt3x2QzRDiD7AxrGw2/1000022718.jpg",
        "body": "Perfectionism is frequently an elegant mask for fear—fear of criticism, fear of failure, or fear of not being good enough. Chasing perfection stalls projects indefinitely, preventing valuable real-world feedback and iteration.\n\nAim for excellent execution rather than flawless perfection in your work today. Remember that a completed project out in the world is infinitely more useful and impactful than a perfect project hidden away in a drawer."
    },
    26: {
        "title": "The Loneliness Epidemic and the Need for Connection",
        "image": "https://cdn.steemitimages.com/DQmSmk3hKKZVux1vqSccPM84U6yHZH8yDtynJdNPbS1ufx8/1000022719.jpg",
        "body": "Despite being more digitally connected than any generation in human history, many people report feeling deeply isolated. Social media interactions often act as a poor substitute for genuine, authentic human relationships.\n\nReach out to an old friend or family member today via a direct phone call or a meaningful message. Investing a few minutes into maintaining your personal support network pays massive dividends for your mental health."
    },
    27: {
        "title": "How Embracing Constraints Fuels Real Innovation",
        "image": "https://cdn.steemitimages.com/DQmXxdzpwdjXmcFJsD9sDUbTC2CXr8mnRHQv4yxJCqprzPk/1000022721.jpg",
        "body": "We often complain about limitations like a lack of time, tight budgets, or minimal resources when working on projects. However, absolute freedom can cause creative paralysis, while clear constraints force us to think innovatively.\n\nInstead of viewing your current limitations as a barrier today, look at them as a creative sandbox. Use your lack of resources as inspiration to find a completely unique, highly resourceful path forward."
    },
    28: {
        "title": "Cultivating Genuine Gratitude During Difficult Times",
        "image": "https://cdn.steemitimages.com/DQmagUVeQJNoT9USdo1RXjK2pNEAL3QkCFea85VEJYmWDQs/1000022720.jpg",
        "body": "Practicing gratitude isn't about wearing toxic positivity glasses or ignoring the very real challenges of your life. It is simply about intentionally training your brain to see the good things that exist right alongside the struggles.\n\nBefore you go to bed tonight, note three specific things that brought a smile to your face today. Shifting your focus to what is working well reduces stress chemicals and improves your overall sleep quality."
    },
    29: {
        "title": "The Invaluable Strength of True Emotional Maturity",
        "image": "https://cdn.steemitimages.com/DQmV8EkxzmQ84GA4fr13QAhP9TEYz3VL6GhBeD2YZFmWJTb/1000022722.jpg",
        "body": "Emotional maturity is defined by the critical gap between experiencing an intense emotion and choosing your reaction. Reacting impulsively out of anger or frustration almost always makes a difficult situation much worse.\n\nWhen someone tests your patience today, take one deep breath before saying a single word. Controlling your immediate reflex allows you to address the problem rationally and de-escalate tension effortlessly."
    },
    30: {
        "title": "The Direct Connection Between Sleep and Daily Success",
        "image": "https://steemitimages.com",
        "body": "Cutting back on sleep to gain extra working hours is a classic trap that rapidly destroys your cognitive processing. Chronic sleep deprivation ruins your mood, kills creativity, and leads to critical decision-making mistakes.\n\nCommit to a relaxing evening wind-down routine tonight by turning off electronic screens thirty minutes before bed. Prioritizing high-quality rest ensures you wake up tomorrow with maximum focus and physical energy."
    },
    31: {
        "title": "Celebrating Your Incremental Progress Over Time",
        "image": "https://steemitimages.com",
        "body": "We are often so entirely focused on the mountain peak ahead that we forget to look back and see how far we climbed. Forgetting to acknowledge your milestones makes the journey feel like an endless, grueling chore.\n\nTake a moment today to recognize a skill or habit you handle easily now that used to challenge you last year. Appreciating your own personal evolution builds the deep internal confidence needed to tackle your next big goal."
    },
    32: {
        "title": "Developing Ultimate Trust in Your Unique Lifepath",
        "image": "https://steemitimages.com",
        "body": "Constantly comparing your milestones to other people's curated social media feeds is a recipe for deep unhappiness. Everyone operates on an entirely unique timeline, shaped by completely different circumstances and goals.\n\nFocus your competitive energy purely on outperforming the person you were yesterday afternoon. Trusting your unique process keeps you grounded, motivated, and fully focused on maximizing your own potential."
    }
    }

# ==========================================
# 4. Dynamic Selection
# ==========================================
# Determine rotation index based on Day of the Year 
# (This ensures a clean 1-32 loop that auto-wraps at the end of cycles)
now_eat = datetime.datetime.utcnow() + datetime.timedelta(hours=3) # UTC to EAT
day_of_year = now_eat.timetuple().tm_yday
selected_index = ((day_of_year - 1) % 32) + 1  

# Human-readable date function
def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

day = now_eat.day
suffix = get_ordinal_suffix(day)
formatted_date = f"{day}{suffix} {now_eat.strftime('%A %B %Y')}"

# Fetch today's unique article elements
article = ARTICLES_POOL[selected_index]

post_title = f"{article['title']} — {formatted_date}"
post_body = f"{article['body']}\n\n{article['image']}"

post_permlink = f"daily-insight-day-{selected_index}-{now_eat.strftime('%Y%m%d')}"
  

# ==========================================
# 5. Connect and broadcast to blockchain
# ==========================================

try:
    print(f"Connecting to node via Cloudflare proxy: {PROXY_URL}")
    
    # Initialize the robust Steem client
    stm = Steem(
        node=[PROXY_URL],
        keys=[MY_PRIVATE_POSTING_KEY]
    )
    
    print(f"Broadcasting Day {selected_index} to community {TARGET_COMMUNITY}.")
    
    # Post directly using the standard blockchain wrapper
    stm.post(
        title=post_title,
        body=post_body,
        author=MY_ACCOUNT,
        permlink=post_permlink,
        tags=[TARGET_COMMUNITY] + CUSTOM_TAGS,
        parent_author="",
        parent_permlink=TARGET_COMMUNITY
    )
    
    print(f"Post #{selected_index} has been published to {TARGET_COMMUNITY}.")

except Exception as e:
    print(f"CRITICAL ERROR: Broadcast routing failed: {e}")
    exit(1)
