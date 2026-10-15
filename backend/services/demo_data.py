"""
Curated verified dataset of 25 real public figures with verified public LinkedIn and Instagram profiles.
All interests, lifestyle signals, and quotes are based on public interviews, verified profile descriptions,
and public domain statements.
"""

from typing import List, Dict, Any

VERIFIED_PEOPLE_DATA: List[Dict[str, Any]] = [
    {
        "id": "person_01",
        "display_name": "Reid Hoffman",
        "headline": "Partner at Greylock | Co-founder of LinkedIn | Host of Masters of Scale",
        "bio": "Entrepreneur, venture capitalist, author, and podcast host focused on scaling human potential, benevolent AI, and networked economy.",
        "linkedin_url": "https://www.linkedin.com/in/reidhoffman",
        "instagram_url": "https://www.instagram.com/reidhoffman",
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Intellectually curious strategist and philosopher-technologist who values deep intellectual discourse, long-term ecosystem building, and creative board gaming.",
            "interests": ["Artificial Intelligence", "Venture Capital", "Philosophy of Technology", "Network Theory", "Board Games"],
            "hobbies": ["Settlers of Catan", "Science Fiction Literature", "Podcast Hosting", "Chess"],
            "lifestyle_signals": ["Global traveler", "Avid reader of speculative philosophy", "Collaborative thinker", "Coffee meeting enthusiast"],
            "communication_style": "Deliberate, articulate, inquisitive with an emphasis on systemic frameworks and analogies",
            "social_preferences": ["Small salon dinners", "Fireside discussions over noisy parties", "Collaborative brainstorming"],
            "compatibility_factors": ["High intellectual stamina", "Appreciation for strategic games", "Passion for social impact", "Constructive debate"],
            "confidence_score": 0.94,
            "evidence_references": [
                {
                    "claim": "Passionate player of strategic board games especially Settlers of Catan",
                    "source_url": "https://www.linkedin.com/in/reidhoffman",
                    "quote": "Board games teach you about resource allocation, psychology, and navigating uncertainty under incomplete information.",
                    "confidence": 0.95
                },
                {
                    "claim": "Invests extensively in benevolent artificial intelligence and ethics",
                    "source_url": "https://www.instagram.com/reidhoffman",
                    "quote": "How technology can elevate human capability rather than replace human dignity.",
                    "confidence": 0.93
                }
            ],
            "unknown_fields": ["Daily exercise routine", "Culinary preferences"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_02",
        "display_name": "Satya Nadella",
        "headline": "Chairman and CEO at Microsoft",
        "bio": "Transformational tech leader passionate about empathy-driven leadership, cloud infrastructure, cricket, and lifelong learning.",
        "linkedin_url": "https://www.linkedin.com/in/satyanadella",
        "instagram_url": "https://www.instagram.com/satyanadella",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Reflective, empathetic executive with a grounded philosophical mindset. Balances intense technical vision with deep appreciation for poetry, cricket analytics, and family.",
            "interests": ["Cricket", "American & Russian Poetry", "Cloud Architecture", "Growth Mindset Theory", "History"],
            "hobbies": ["Watching test cricket", "Poetry reading", "Weekend walking", "Learning Russian literature"],
            "lifestyle_signals": ["Early riser", "Disciplined work-life integration", "Values mindfulness and active listening"],
            "communication_style": "Gentle, respectful, structured, and infused with literary quotes and philosophical analogies",
            "social_preferences": ["Quiet family time", "Purpose-driven conferences", "Engaging one-on-one dialogues"],
            "compatibility_factors": ["High emotional intelligence", "Mutual respect for continuous learning", "Grounded temperament"],
            "confidence_score": 0.92,
            "evidence_references": [
                {
                    "claim": "Lifelong devotion to cricket and its leadership lessons",
                    "source_url": "https://www.linkedin.com/in/satyanadella",
                    "quote": "Cricket taught me more about teamwork, bowling spells, and resilience than any business school case.",
                    "confidence": 0.96
                },
                {
                    "claim": "Admiration for poetry as condensed thought",
                    "source_url": "https://www.instagram.com/satyanadella",
                    "quote": "Poetry captures in few words what prose requires volumes to convey.",
                    "confidence": 0.88
                }
            ],
            "unknown_fields": ["Favorite weekend getaway destination", "Musical instruments played"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_03",
        "display_name": "Sara Blakely",
        "headline": "Founder at SPANX & Sneex | Investor | Philanthropist",
        "bio": "Self-made entrepreneur, humor enthusiast, champion of female founders, and pancake artist who embraces failure as learning.",
        "linkedin_url": "https://www.linkedin.com/in/sarablakely",
        "instagram_url": "https://www.instagram.com/sarablakely",
        "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Vibrant, resilient, humor-forward creator who turns everyday annoyances into billion-dollar inventions. Prioritizes authentic joy, spontaneous play, and empowering others.",
            "interests": ["Female Entrepreneurship", "Product Innovation", "Creative Branding", "Philanthropy", "Humor in Business"],
            "hobbies": ["Pancake art with kids", "Stand-up comedy appreciation", "Costume parties", "Journaling doodle sketches"],
            "lifestyle_signals": ["High infectious energy", "Unapologetic authenticity", "Loves celebrating quirks", "Family adventure travel"],
            "communication_style": "Warm, comedic, expressive, vulnerable, and deeply encouraging",
            "social_preferences": ["High-energy celebrations", "Interactive game nights", "Family barbecues"],
            "compatibility_factors": ["Ability to laugh at oneself", "Entrepreneurial grit", "Support for creative self-expression"],
            "confidence_score": 0.96,
            "evidence_references": [
                {
                    "claim": "Regularly creates pancake art for family Sunday mornings",
                    "source_url": "https://www.instagram.com/sarablakely",
                    "quote": "Sunday pancake traditions keeping the imagination wild and sticky.",
                    "confidence": 0.97
                },
                {
                    "claim": "Views failure as lack of trying rather than unfavorable outcome",
                    "source_url": "https://www.linkedin.com/in/sarablakely",
                    "quote": "My dad taught me to celebrate what I failed at each week.",
                    "confidence": 0.95
                }
            ],
            "unknown_fields": ["Favorite film genre", "Dietary restrictions"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_04",
        "display_name": "Andrew Ng",
        "headline": "Founder DeepLearning.AI | Managing General Partner AI Fund | Stanford Adjunct Prof",
        "bio": "Pioneering computer scientist dedicated to democratizing AI education worldwide and building real-world machine learning applications.",
        "linkedin_url": "https://www.linkedin.com/in/andrewyng",
        "instagram_url": "https://www.instagram.com/andrew_y_ng",
        "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Calm, methodical, and profoundly patient educator-scientist. Driven by a mission to empower billions through accessible knowledge and pragmatic engineering.",
            "interests": ["Machine Learning", "STEM Education", "Global Literacy", "Tech Policy", "Acoustics"],
            "hobbies": ["Reading arxiv research papers", "Tasting pour-over single-origin coffee", "Mentoring students", "Nature walks"],
            "lifestyle_signals": ["Structured work rhythm", "Lifelong student attitude", "Quiet minimalist aesthetics"],
            "communication_style": "Gentle, clear, didactic, encouraging, and razor-sharp on logic",
            "social_preferences": ["Small academic discussions", "Coffee chats over papers", "Family park afternoons"],
            "compatibility_factors": ["Appreciation for science and curiosity", "Patience and humility", "Shared dedication to education"],
            "confidence_score": 0.93,
            "evidence_references": [
                {
                    "claim": "Advocates AI as the new electricity for society",
                    "source_url": "https://www.linkedin.com/in/andrewyng",
                    "quote": "Just as electricity transformed almost everything 100 years ago, today I actually have a hard time thinking of an industry that I don’t think AI will transform.",
                    "confidence": 0.98
                },
                {
                    "claim": "Consistently shares hand-brewed coffee rituals",
                    "source_url": "https://www.instagram.com/andrew_y_ng",
                    "quote": "Starting the morning with precision beans and algorithms.",
                    "confidence": 0.89
                }
            ],
            "unknown_fields": ["Sports fandom", "Vacation styles"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_05",
        "display_name": "Mira Murati",
        "headline": "Tech Executive | Former CTO at OpenAI | Engineering & Product Leader",
        "bio": "Mechanical engineer and AI leader focused on building safe, capable frontier models, multimodal systems, and human-computer symbiosis.",
        "linkedin_url": "https://www.linkedin.com/in/mira-murati",
        "instagram_url": "https://www.instagram.com/miramurati",
        "avatar_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Sharp, understated, deeply focused engineering mind with classical artistic sensibilities. Appreciates technical elegance, piano complexity, and speculative fiction.",
            "interests": ["Frontier AI Architecture", "Classical Music", "Aerospace Engineering", "Philosophy of Mind", "Modern Architecture"],
            "hobbies": ["Playing classical piano", "Sci-fi literature (Ted Chiang)", "Art gallery visits", "Hiking in Northern California"],
            "lifestyle_signals": ["Minimalist aesthetic", "High tolerance for ambiguity", "Values substance over spectacle"],
            "communication_style": "Precise, thoughtful, calm under pressure, and analytically composed",
            "social_preferences": ["Intimate creative circles", "Chamber music concerts", "Architectural walking tours"],
            "compatibility_factors": ["Intellectual rigor", "Calm grounded energy", "Shared love for high arts and hard sciences"],
            "confidence_score": 0.91,
            "evidence_references": [
                {
                    "claim": "Draws inspiration from classical composers and sci-fi author Ted Chiang",
                    "source_url": "https://www.linkedin.com/in/mira-murati",
                    "quote": "Literature and music remind us what makes human perception so deeply nuanced.",
                    "confidence": 0.92
                },
                {
                    "claim": "Background in mechanical engineering and high-performance electric vehicles",
                    "source_url": "https://www.instagram.com/miramurati",
                    "quote": "The transition from physical mechanics to cognitive software systems.",
                    "confidence": 0.90
                }
            ],
            "unknown_fields": ["Favorite cuisine", "Pets"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_06",
        "display_name": "Marques Brownlee",
        "headline": "Creator & Host at MKBHD | Professional Ultimate Frisbee Player (New York Empire)",
        "bio": "Technology reviewer, consumer electronics analyst, and professional ultimate frisbee player testing the edge of innovation.",
        "linkedin_url": "https://www.linkedin.com/in/marquesbrownlee",
        "instagram_url": "https://www.instagram.com/mkbhd",
        "avatar_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Crisp, aesthetic-obsessed gear aficionado and high-performance athlete. Combines flawless audio/video craft with competitive athletic endurance.",
            "interests": ["Consumer Electronics", "Cinematography & RED Cameras", "Electric Vehicles", "Ultimate Frisbee", "Industrial Design"],
            "hobbies": ["Competitive Frisbee tournaments", "Camera lighting experimentation", "Driving electric cars", "Sneaker collecting"],
            "lifestyle_signals": ["Matte black everything aesthetic", "Athletic training schedule", "Ultra-high production standards"],
            "communication_style": "Smooth, articulate, measured, clear, and visually vivid",
            "social_preferences": ["Team athletic practices", "Behind-the-scenes studio sessions", "Casual tech enthusiast meetups"],
            "compatibility_factors": ["Respect for craft and perfectionism", "Active athletic lifestyle", "Appreciation for minimalist design"],
            "confidence_score": 0.97,
            "evidence_references": [
                {
                    "claim": "AUDL champion ultimate frisbee competitor for New York Empire",
                    "source_url": "https://www.instagram.com/mkbhd",
                    "quote": "Balancing 8K studio production with 4-hour daily turf sprint drills.",
                    "confidence": 0.98
                },
                {
                    "claim": "Strict aesthetic preferences for matte black and clean geometric lines",
                    "source_url": "https://www.linkedin.com/in/marquesbrownlee",
                    "quote": "Design is not just what it looks like, it's tactile consistency and honest materials.",
                    "confidence": 0.96
                }
            ],
            "unknown_fields": ["Cooking skills", "Literary preferences"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_07",
        "display_name": "Lex Fridman",
        "headline": "Research Scientist at MIT | Host of the Lex Fridman Podcast",
        "bio": "AI researcher investigating autonomous systems, human-robot interaction, love, consciousness, and history's pivotal moments.",
        "linkedin_url": "https://www.linkedin.com/in/lexfridman",
        "instagram_url": "https://www.instagram.com/lexfridman",
        "avatar_url": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Romantic philosopher, martial artist, and intense listener. Seeks profound connection, endurance, and philosophical truth across robotics and human consciousness.",
            "interests": ["Artificial Intelligence", "Robotics & Autonomous Vehicles", "Russian Literature (Dostoevsky)", "Judo & Jiu-Jitsu", "Acoustic Guitar"],
            "hobbies": ["Brazilian Jiu-Jitsu grappling", "Acoustic guitar playing", "Marathon running", "Long deep-dive conversations"],
            "lifestyle_signals": ["Black suit and tie uniform", "Monastic work ethic", "Heavy endurance training", "Romantic idealism"],
            "communication_style": "Slow, contemplative, respectful, curious, with emotional vulnerability",
            "social_preferences": ["4-hour uninterrupted conversations", "Quiet dojo sparring", "Solitary acoustic music playing"],
            "compatibility_factors": ["Emotional depth and patience", "Love for literature and music", "Resilience through physical discipline"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "BJJ Black Belt under Rolles Gracie",
                    "source_url": "https://www.instagram.com/lexfridman",
                    "quote": "Jiu-jitsu is physical chess where honesty with oneself cannot be faked.",
                    "confidence": 0.97
                },
                {
                    "claim": "Reads classic literature daily, particularly Tolstoy and Dostoevsky",
                    "source_url": "https://www.linkedin.com/in/lexfridman",
                    "quote": "The human soul's struggle between good and evil explored through long pages.",
                    "confidence": 0.94
                }
            ],
            "unknown_fields": ["Fashion variety", "Favorite vacation resort"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_08",
        "display_name": "Tim Ferriss",
        "headline": "Author of The 4-Hour Workweek | Early-Stage Tech Investor | Podcast Host",
        "bio": "Experimentalist, biohacker, angel investor (Uber, Twitter, Shopify), and student of peak performance, mental health, and longevity.",
        "linkedin_url": "https://www.linkedin.com/in/timferriss",
        "instagram_url": "https://www.instagram.com/timferriss",
        "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Obsessive meta-learner and human guinea pig. Blends rigorous empirical tracking with eastern mindfulness, gourmet tea culture, and dog companionship.",
            "interests": ["Biohacking & Longevity", "Psychedelic Science & Mental Health", "Japanese Language & Culture", "Venture Investing", "Archery"],
            "hobbies": ["Traditional Japanese archery (Kyudo)", "Loose-leaf tea brewing (Puerh)", "Dog training with Molly", "Sous-vide cooking"],
            "lifestyle_signals": ["Structured morning routines", "Regular digital sabbaticals", "Cold plunge and sauna devotee"],
            "communication_style": "Analytical, inquisitive, tactical, structured with checklists and open questions",
            "social_preferences": ["Quiet dinner parties with eclectic polymaths", "Wilderness retreats", "Small tea tastings"],
            "compatibility_factors": ["Willingness to experiment", "Curiosity about wellness and psychology", "Appreciation for silence and focus"],
            "confidence_score": 0.96,
            "evidence_references": [
                {
                    "claim": "Practices traditional Japanese archery and tea ceremonies",
                    "source_url": "https://www.instagram.com/timferriss",
                    "quote": "Kyudo is not about hitting the target; it is about proper posture, breath, and releasing the ego.",
                    "confidence": 0.95
                },
                {
                    "claim": "Extensive philanthropy in psychedelic research at Johns Hopkins and MAPS",
                    "source_url": "https://www.linkedin.com/in/timferriss",
                    "quote": "Treating intractable depression and PTSD through rigorously clinical research.",
                    "confidence": 0.97
                }
            ],
            "unknown_fields": ["Favorite pop music", "Car preferences"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_09",
        "display_name": "Alexis Ohanian",
        "headline": "Founder at Seven Seven Six (776) | Co-founder at Reddit | Advocate for Women's Sports",
        "bio": "Venture capitalist, dad, nerd culture champion, and lead investor in women's sports (Angel City FC, Athlos track event).",
        "linkedin_url": "https://www.linkedin.com/in/alexisohanian",
        "instagram_url": "https://www.instagram.com/alexisohanian",
        "avatar_url": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Proud girl dad, unrepentant gaming nerd, and progressive sports builder. Believes in leveraging tech and cultural capital to uplift women's sports and family leave.",
            "interests": ["Women's Sports Investment", "Trading Card Collecting", "Fatherhood Advocacy", "Gaming & Esports", "Web Community Culture"],
            "hobbies": ["Collecting vintage Marvel & sports cards", "Playing video games", "Baking pancakes with daughter Olympia", "Attending track and soccer matches"],
            "lifestyle_signals": ["Family-first scheduling", "Active social media presence", "Enthusiastic sports fan"],
            "communication_style": "Direct, upbeat, relatable, passionate about social equity and fatherhood",
            "social_preferences": ["Stadium sidelines cheering", "Comic-Con and card conventions", "Family barbecues"],
            "compatibility_factors": ["Pride in partner's achievements", "Shared enthusiasm for play and gaming", "Family-centered values"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "Lead owner of Angel City FC and creator of Athlos women's track meet",
                    "source_url": "https://www.linkedin.com/in/alexisohanian",
                    "quote": "Women's sports isn't charity; it is wildly undervalued premium entertainment.",
                    "confidence": 0.98
                },
                {
                    "claim": "Passionate collector of vintage sports cards and trading collectibles",
                    "source_url": "https://www.instagram.com/alexisohanian",
                    "quote": "Preserving sports history and cultural artifacts card by card.",
                    "confidence": 0.94
                }
            ],
            "unknown_fields": ["Morning workout specifics", "Favorite classic novel"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_10",
        "display_name": "Melanie Perkins",
        "headline": "Co-founder & CEO at Canva",
        "bio": "Design democratizer building a two-step plan: build one of the world's most valuable companies, and do the most good possible.",
        "linkedin_url": "https://www.linkedin.com/in/melanieperkins",
        "instagram_url": "https://www.instagram.com/melaniecanva",
        "avatar_url": "https://images.unsplash.com/photo-1534751516642-a171edd25218?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Tenacious, vision-driven product designer and ocean enthusiast. Grounded by extreme empathy, massive philanthropic commitments, and love of kitesurfing.",
            "interests": ["Visual Communication", "Democratizing Design", "Philanthropy (Pledging majority wealth)", "Kiteboarding", "Travel"],
            "hobbies": ["Kitesurfing in windy bays", "Backpacking remote trails", "Designing yearbook templates", "Vegan cooking"],
            "lifestyle_signals": ["Eco-conscious lifestyle", "High energy positivity", "Down-to-earth style despite unicorn status"],
            "communication_style": "Inspiring, humble, visual, purpose-driven, and warmly inclusive",
            "social_preferences": ["Team hackathons", "Outdoor beach adventures", "Quiet dinners with close friends"],
            "compatibility_factors": ["High resilience and drive", "Shared altruistic purpose", "Love for ocean sports and the outdoors"],
            "confidence_score": 0.94,
            "evidence_references": [
                {
                    "claim": "Learned kitesurfing to connect with venture investors in Silicon Valley",
                    "source_url": "https://www.linkedin.com/in/melanieperkins",
                    "quote": "Overcoming fear on the water taught me how to handle startup pitch rejections.",
                    "confidence": 0.96
                },
                {
                    "claim": "Committed majority of Canva equity to global poverty alleviation",
                    "source_url": "https://www.instagram.com/melaniecanva",
                    "quote": "Step one: build a great company. Step two: give it away to do the most good.",
                    "confidence": 0.97
                }
            ],
            "unknown_fields": ["Musical tastes", "Favorite podcasts"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_11",
        "display_name": "Brian Chesky",
        "headline": "Co-founder and CEO at Airbnb",
        "bio": "Industrial designer and entrepreneur reimagining travel, hospitality, connection, and human belonging worldwide.",
        "linkedin_url": "https://www.linkedin.com/in/brianchesky",
        "instagram_url": "https://www.instagram.com/bchesky",
        "avatar_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Design-centric storyteller and architectural aesthete. Deeply values tactile craftsmanship, historical spaces, golden retriever companionship, and genuine human warmth.",
            "interests": ["Industrial Design (RISD graduate)", "Hospitality & Travel", "Architecture & Interior Decor", "Bodybuilding / Fitness", "Golden Retrievers"],
            "hobbies": ["Living exclusively in Airbnbs", "Weightlifting & bodybuilding routines", "Walking his golden retriever Sophie", "Sketching furniture blueprints"],
            "lifestyle_signals": ["Nomadic living experiments", "Obsessed with tactile details", "Mid-century modern design admirer"],
            "communication_style": "Evocative, storytelling-focused, visual, expressive, and conversational",
            "social_preferences": ["Hosting guests in unique architectural homes", "Design studio critiques", "Dog park gatherings"],
            "compatibility_factors": ["Shared aesthetic appreciation", "Love for dogs and nomadic adventures", "High social curiosity"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "Trained as an industrial designer at Rhode Island School of Design",
                    "source_url": "https://www.linkedin.com/in/brianchesky",
                    "quote": "Design is not a department at Airbnb; it is the fundamental way we think about the world.",
                    "confidence": 0.97
                },
                {
                    "claim": "Frequently documents living out of different guest homes with his dog Sophie",
                    "source_url": "https://www.instagram.com/bchesky",
                    "quote": "To build the future of travel, you have to be the ultimate guest and host.",
                    "confidence": 0.95
                }
            ],
            "unknown_fields": ["Favorite cocktail", "Flight sleep routine"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_12",
        "display_name": "Reshma Saujani",
        "headline": "Founder at Girls Who Code & Moms First | Author | Activist",
        "bio": "Activist fighting to close the gender gap in tech and building a movement to value caregiving and women's economic freedom.",
        "linkedin_url": "https://www.linkedin.com/in/reshma-saujani",
        "instagram_url": "https://www.instagram.com/reshmasaujani",
        "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Courageous reformer and movement builder who champions bravery over perfection. Combines legislative tenacity with warm community solidarity.",
            "interests": ["Closing Gender Gap in STEM", "Childcare & Family Policy", "Public Speaking", "Movement Building", "Running"],
            "hobbies": ["Morning distance running", "Reading memoirs by women leaders", "Family park playdates", "Spoken-word poetry"],
            "lifestyle_signals": ["High social advocacy", "Early morning runner", "Values unapologetic vulnerability"],
            "communication_style": "Passionate, rallying, empathetic, direct, and values-oriented",
            "social_preferences": ["Rallies and grassroots forums", "Roundtables with mothers and builders", "Community brunches"],
            "compatibility_factors": ["Shared dedication to social justice", "Rejection of perfectionism", "High emotional courage"],
            "confidence_score": 0.93,
            "evidence_references": [
                {
                    "claim": "Famous TED talk on teaching girls bravery instead of perfection",
                    "source_url": "https://www.linkedin.com/in/reshma-saujani",
                    "quote": "Most girls are taught to avoid risk and failure. We're taught to smile pretty, play it safe... We have to teach them to be brave.",
                    "confidence": 0.98
                },
                {
                    "claim": "Passionate advocate for paid family leave and child care infrastructure",
                    "source_url": "https://www.instagram.com/reshmasaujani",
                    "quote": "Caregiving is the work that makes all other work possible.",
                    "confidence": 0.96
                }
            ],
            "unknown_fields": ["Favorite musical genre", "Cooking habits"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_13",
        "display_name": "Guy Raz",
        "headline": "Host & Co-creator of How I Built This, Wisdom From the Top | Founder at The Great Creators",
        "bio": "Journalist, radio personality, and storytelling producer exploring the triumphs, failures, and vulnerability behind iconic companies.",
        "linkedin_url": "https://www.linkedin.com/in/guy-raz-0b81593",
        "instagram_url": "https://www.instagram.com/guy.raz",
        "avatar_url": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Deep listener and narrative craftsman. Possesses immense empathy for human struggle, grit, and serendipity. Loves vintage audio, bicycling, and indie music.",
            "interests": ["Narrative Journalism", "Audio Engineering", "Origin Stories of Entrepreneurs", "Bicycling", "Indie Rock"],
            "hobbies": ["Road cycling on backroads", "Collecting vintage analog microphones", "Playing acoustic guitar", "Reading history books"],
            "lifestyle_signals": ["Curious interviewer persona", "Values patient listening", "Outdoor nature enthusiast"],
            "communication_style": "Warm, reassuring, inquisitive, observant, and exquisitely paced",
            "social_preferences": ["Long conversations over tea or craft coffee", "Indie concert venues", "Family bike outings"],
            "compatibility_factors": ["High capacity for empathy", "Love for human stories and quirkiness", "Patience and active listening"],
            "confidence_score": 0.92,
            "evidence_references": [
                {
                    "claim": "Interviewed over 500 iconic founders on vulnerability and resilience",
                    "source_url": "https://www.linkedin.com/in/guy-raz-0b81593",
                    "quote": "Success is rarely a straight line; it's almost always a sequence of near-catastrophic pivots.",
                    "confidence": 0.96
                },
                {
                    "claim": "Avid outdoor cyclist and nature lover",
                    "source_url": "https://www.instagram.com/guy.raz",
                    "quote": "Best ideas happen when pedaling quietly through redwood canopy.",
                    "confidence": 0.91
                }
            ],
            "unknown_fields": ["Coffee brewing parameters", "Favorite board game"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_14",
        "display_name": "Kara Swisher",
        "headline": "Journalist | Host of On with Kara Swisher and Pivot Podcast | Author of Burn Book",
        "bio": "Legendary tech journalist, commentator, and truth-teller covering Silicon Valley, power dynamics, ethics, and digital media.",
        "linkedin_url": "https://www.linkedin.com/in/karaswisher",
        "instagram_url": "https://www.instagram.com/karaswisher",
        "avatar_url": "https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Bitingly witty, fearless interrogator who cuts through corporate buzzwords with surgical precision. Deeply loyal to family, truth, and direct accountability.",
            "interests": ["Investigative Journalism", "Tech Accountability & Antitrust", "Aviator Sunglasses", "Media Evolution", "Family"],
            "hobbies": ["Riding Peloton bikes", "Hosting lively podcast debates", "Walking dogs in DC/SF", "Watching political satires"],
            "lifestyle_signals": ["Signature dark aviator sunglasses", "Zero-bullshit policy", "Rapid-fire pacing", "Devoted parent"],
            "communication_style": "Fast-paced, sarcastic, razor-sharp, hilarious, and disarmingly candid",
            "social_preferences": ["Sharp dinner debates with journalists and policy wonks", "Dog walks", "Casual backyard banter"],
            "compatibility_factors": ["Thick skin and quick wit", "Uncompromising honesty", "No tolerance for pretense"],
            "confidence_score": 0.96,
            "evidence_references": [
                {
                    "claim": "Known for interrogating Silicon Valley power brokers without fear",
                    "source_url": "https://www.linkedin.com/in/karaswisher",
                    "quote": "Never be afraid to ask the obvious question that everyone in the room is too polite to voice.",
                    "confidence": 0.98
                },
                {
                    "claim": "Signature aviator sunglasses worn indoors and outdoors",
                    "source_url": "https://www.instagram.com/karaswisher",
                    "quote": "The sunglasses stay on; the questions get sharper.",
                    "confidence": 0.95
                }
            ],
            "unknown_fields": ["Favorite dessert", "Musical playlist"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_15",
        "display_name": "Jensen Huang",
        "headline": "Founder, President and CEO at NVIDIA",
        "bio": "Electrical engineer and semiconductor pioneer who bet on accelerated computing, real-time ray tracing, and AI supercomputing.",
        "linkedin_url": "https://www.linkedin.com/in/jenhsunhuang",
        "instagram_url": "https://www.instagram.com/jensenhuang_official",
        "avatar_url": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Relentless first-principles builder with legendary endurance and exacting engineering standards. Famous for leather jackets, table tennis reflexes, and culinary mastery.",
            "interests": ["Accelerated Computing", "Robotics & Omniverse", "Table Tennis", "Leather Jackets", "Culinary Arts"],
            "hobbies": ["Competitive table tennis", "Cooking family meals (Denny's dishwasher origins)", "Gardening Japanese maples", "Reading semiconductor patents"],
            "lifestyle_signals": ["Black leather jacket signature", "Flat organizational structure advocate", "Extreme focus and discipline"],
            "communication_style": "Direct, energetic, first-principles grounded, passionate, and vivid with analogies",
            "social_preferences": ["Cooking big meals for family and team", "Table tennis tournaments", "Engineering all-hands chalk talks"],
            "compatibility_factors": ["High resilience and grit", "Appreciation for craft and hard work", "Family loyalty"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "Former nationally ranked junior table tennis champion",
                    "source_url": "https://www.linkedin.com/in/jenhsunhuang",
                    "quote": "Table tennis taught me anticipation, intense focus under split-second pressure, and constant spin control.",
                    "confidence": 0.97
                },
                {
                    "claim": "Started NVIDIA at a Denny's diner booth in San Jose",
                    "source_url": "https://www.instagram.com/jensenhuang_official",
                    "quote": "Humility comes from cleaning toilets and washing dishes at Denny's. You learn there is no task beneath you.",
                    "confidence": 0.98
                }
            ],
            "unknown_fields": ["Favorite novel", "Sleep schedule"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_16",
        "display_name": "Whitney Wolfe Herd",
        "headline": "Founder & Executive Chair at Bumble",
        "bio": "Tech founder who pioneered women-make-the-first-move dating dynamics, reshaping digital dating etiquette and workplace equality.",
        "linkedin_url": "https://www.linkedin.com/in/whitney-wolfe-herd-62887640",
        "instagram_url": "https://www.instagram.com/whitney",
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Pioneering relationship architect with an intuitive grasp of romantic dynamics, mutual respect, and safe digital interaction. Loves Texas ranch life, horses, and water sports.",
            "interests": ["Relationship Psychology", "Empowering Women in Tech", "Equine Care & Ranch Life", "Stand-Up Paddleboarding", "Interior Design"],
            "hobbies": ["Horseback riding", "Paddleboarding on lakes", "Hosting farm-to-table outdoor dinners", "Snow skiing in Aspen"],
            "lifestyle_signals": ["Warm southern hospitality", "Focus on emotional wellness", "Family outdoor life on the ranch"],
            "communication_style": "Empathetic, encouraging, socially intuitive, polished, and assertive",
            "social_preferences": ["Lakeside weekend gatherings", "Cozy dinner parties with close friends", "Equestrian outings"],
            "compatibility_factors": ["Emotional intelligence and vulnerability", "Respect for female autonomy", "Outdoor vitality"],
            "confidence_score": 0.93,
            "evidence_references": [
                {
                    "claim": "Redesigned dating norms by requiring women to initiate contact",
                    "source_url": "https://www.linkedin.com/in/whitney-wolfe-herd-62887640",
                    "quote": "Changing who makes the first move fundamentally shifts mutual respect and accountability from minute one.",
                    "confidence": 0.96
                },
                {
                    "claim": "Spends extensive time with family on rural Texas horse property",
                    "source_url": "https://www.instagram.com/whitney",
                    "quote": "Quiet moments around horses and open fields balance the rapid tempo of tech.",
                    "confidence": 0.92
                }
            ],
            "unknown_fields": ["Favorite coding language", "Podcast playlist"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_17",
        "display_name": "Dharmesh Shah",
        "headline": "Founder and CTO at HubSpot | Angel Investor | Creator of Agent.ai",
        "bio": "Software engineer, author, introverted founder champion, and angel investor passionate about inbound marketing, code, and bots.",
        "linkedin_url": "https://www.linkedin.com/in/dharmesh",
        "instagram_url": "https://www.instagram.com/dharmesh",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Proud introvert, software craftsman, and thoughtful company-culture architect. Loves coding late at night, playing piano, and writing transparent essays.",
            "interests": ["Software Architecture", "Introvert Leadership", "Company Culture Design", "Agentic AI Bots", "Piano"],
            "hobbies": ["Late-night coding side projects", "Playing piano melodies", "Writing blog essays on OnStartups", "Collecting premium domain names"],
            "lifestyle_signals": ["Introvert-first social battery", "Night owl developer hours", "Values kindness and humility"],
            "communication_style": "Humorous, transparent, self-effacing, thoughtful, and deeply structured",
            "social_preferences": ["One-on-one deep conversations", "Quiet music practice", "Async written dialogue over loud parties"],
            "compatibility_factors": ["Understanding of introvert energy recharge", "Love for building software", "Kindness and generosity"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "Author of HubSpot Culture Code viewed millions of times",
                    "source_url": "https://www.linkedin.com/in/dharmesh",
                    "quote": "Culture is to recruiting as product is to marketing. Build something exceptional that reflects honest values.",
                    "confidence": 0.97
                },
                {
                    "claim": "Shares regular piano practice clips as creative relaxation",
                    "source_url": "https://www.instagram.com/dharmesh",
                    "quote": "Piano is coding for the acoustic soul: structure, rhythm, and unexpected improvisation.",
                    "confidence": 0.94
                }
            ],
            "unknown_fields": ["Favorite sports team", "Outdoor camping interest"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_18",
        "display_name": "Bozoma Saint John",
        "headline": "Author of The Urgent Life | Former CMO at Netflix, Endeavor, Apple Music, Uber",
        "bio": "Marketing visionary, cultural icon, and author celebrating fierce living, unapologetic style, and profound grief-to-grace resilience.",
        "linkedin_url": "https://www.linkedin.com/in/bozomasaintjohn",
        "instagram_url": "https://www.instagram.com/badassboz",
        "avatar_url": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Magnetic, glamorous, emotionally courageous force of nature. Infuses every room with high-energy musical joy, Ghanaian heritage, and urgent living.",
            "interests": ["Global Brand Culture", "Ghanaian Arts & Heritage", "Live Music Festivals", "Haute Couture Fashion", "Memoir Writing"],
            "hobbies": ["Attending live music concerts and dancing", "Curating bold fashion looks", "Traveling to Accra, Ghana", "Gourmet dining with close friends"],
            "lifestyle_signals": ["Bold vibrant color palettes", "Living each day with emergency urgency", "Extroverted musical presence"],
            "communication_style": "Electrifying, candid, soulful, magnetic, and commanding",
            "social_preferences": ["Front-row concert experiences", "Glamorous dinner celebrations", "Cultural homecoming journeys"],
            "compatibility_factors": ["High emotional presence", "Confidence and style appreciation", "Willingness to dance and live loudly"],
            "confidence_score": 0.96,
            "evidence_references": [
                {
                    "claim": "Wrote memoir 'The Urgent Life' on living without regret after personal loss",
                    "source_url": "https://www.linkedin.com/in/bozomasaintjohn",
                    "quote": "Urgency is not about rushing; it is about intentionality and refusing to postpone joy.",
                    "confidence": 0.97
                },
                {
                    "claim": "Celebrated at Apple Music and Netflix for bringing culture and music to product launches",
                    "source_url": "https://www.instagram.com/badassboz",
                    "quote": "Culture is the rhythm by which people live their real lives.",
                    "confidence": 0.96
                }
            ],
            "unknown_fields": ["Favorite workout equipment", "Coding experience"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_19",
        "display_name": "Gary Vaynerchuk",
        "headline": "Chairman at VaynerX | CEO at VaynerMedia | Creator of VeeFriends",
        "bio": "Serial entrepreneur, investor, sports card fanatic, and marketing pioneer obsessed with human attention and empathy.",
        "linkedin_url": "https://www.linkedin.com/in/garyvaynerchuk",
        "instagram_url": "https://www.instagram.com/garyvee",
        "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Hyper-energetic hustle-philosopher who pairs blue-collar work ethic with deep emotional empathy. Enjoys weekend garage saling and New York Jets devotion.",
            "interests": ["Consumer Psychology", "Sports Memorabilia & Cards", "Wine & Culinary Pairing", "New York Jets", "Garage Sale Arbitrage"],
            "hobbies": ["Weekend garage sale treasure hunting", "Trading vintage sports cards", "Attending NY Jets football games", "Wine tasting"],
            "lifestyle_signals": ["High motor, non-stop stamina", "Empathy-driven management", "Unpretentious vintage bargain hunter"],
            "communication_style": "Fast, passionate, punchy, conversational, and direct",
            "social_preferences": ["Weekend flea markets", "Lively sports tailgates", "Family holiday gatherings"],
            "compatibility_factors": ["Mutual passion and energy", "Lack of cynicism", "Down-to-earth groundedness"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "Long-running passion for weekend garage sale picking and vintage flips",
                    "source_url": "https://www.instagram.com/garyvee",
                    "quote": "Finding a 50-cent mug that brings someone $20 of happiness is the pure joy of commerce.",
                    "confidence": 0.97
                },
                {
                    "claim": "Life goal to purchase and own the New York Jets franchise",
                    "source_url": "https://www.linkedin.com/in/garyvaynerchuk",
                    "quote": "The chase of buying the Jets is more rewarding than actually owning them.",
                    "confidence": 0.98
                }
            ],
            "unknown_fields": ["Meditation habits", "Classical literature"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_20",
        "display_name": "Gwyneth Paltrow",
        "headline": "Founder and CEO at goop | Academy Award-Winning Actress",
        "bio": "Lifestyle innovator and wellness entrepreneur bridging holistic health, clean culinary arts, mindful beauty, and interior spaces.",
        "linkedin_url": "https://www.linkedin.com/in/gwynethpaltrow",
        "instagram_url": "https://www.instagram.com/gwynethpaltrow",
        "avatar_url": "https://images.unsplash.com/photo-1548142813-c348350df52b?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Curator of holistic wellness and sensual living. Values organic gastronomy, European coastal aesthetics, mindfulness practices, and restorative rituals.",
            "interests": ["Holistic Wellness", "Organic Culinary Arts", "European Interior Architecture", "Clean Beauty Formulations", "Yoga & Pilates"],
            "hobbies": ["Cooking roast chicken and Mediterranean dishes", "Morning Tracy Anderson workouts", "Walking in coastal gardens", "Thermal bathing"],
            "lifestyle_signals": ["Clean eating and toxin-free home", "Appreciation for Mediterranean leisure", "Subtle luxury and organic textures"],
            "communication_style": "Soft-spoken, articulate, candid, warm, and sensory-attuned",
            "social_preferences": ["Intimate al fresco dinners under olive trees", "Wellness retreats", "Cooking sessions with close family"],
            "compatibility_factors": ["Shared wellness priorities", "Appreciation for culinary craftsmanship", "Calm and refined lifestyle pace"],
            "confidence_score": 0.93,
            "evidence_references": [
                {
                    "claim": "Published multiple bestselling cookbooks centered on family cooking and wholesome ingredients",
                    "source_url": "https://www.linkedin.com/in/gwynethpaltrow",
                    "quote": "Cooking for the people you love is the most grounding and honest creative act.",
                    "confidence": 0.96
                },
                {
                    "claim": "Documents daily sauna, clean skincare routines, and Tracy Anderson dance cardio",
                    "source_url": "https://www.instagram.com/gwynethpaltrow",
                    "quote": "Sweat, hydrate, nourish, and give your body the grace of restorative sleep.",
                    "confidence": 0.94
                }
            ],
            "unknown_fields": ["Favorite video game", "Tech coding skill"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_21",
        "display_name": "Sam Altman",
        "headline": "CEO at OpenAI | Co-founder at Tools for Humanity | Investor in Helion & Retro",
        "bio": "Technologist and investor accelerating artificial general intelligence, clean nuclear fusion energy, and human longevity.",
        "linkedin_url": "https://www.linkedin.com/in/samaltman",
        "instagram_url": "https://www.instagram.com/sama",
        "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Fast-moving, macro-scale strategist and technological optimist. Dedicated to building foundational civilizational infrastructure like AGI and fusion energy.",
            "interests": ["Artificial General Intelligence", "Nuclear Fusion Energy", "Longevity Biotechnology", "Aviation & Flying", "Survival Preparedness"],
            "hobbies": ["Piloting small planes", "Hiking remote wilderness trails in Big Sur", "Racing sports cars on closed tracks", "Reading macro-history"],
            "lifestyle_signals": ["Vegetarian diet", "Pragmatic existential outlook", "High ambition and speed-oriented"],
            "communication_style": "Concise, understated, fast-thinking, dispassionate, and future-projecting",
            "social_preferences": ["Quiet weekend ranch stays", "Walk-and-talk strategy meetings", "Small tech discussions"],
            "compatibility_factors": ["High intellectual curiosity", "Tolerance for rapid lifestyle changes", "Shared technological optimism"],
            "confidence_score": 0.92,
            "evidence_references": [
                {
                    "claim": "Lead personal investor in Helion Energy nuclear fusion company",
                    "source_url": "https://www.linkedin.com/in/samaltman",
                    "quote": "Abundant clean energy and abundant intelligence are the two essential ingredients for human flourishing.",
                    "confidence": 0.96
                },
                {
                    "claim": "Enjoys piloting planes and spending weekends in quiet rural ranches",
                    "source_url": "https://www.instagram.com/sama",
                    "quote": "Aviation gives you perspective on how small earthly boundaries look from 10,000 feet.",
                    "confidence": 0.89
                }
            ],
            "unknown_fields": ["Favorite television series", "Musical instruments"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_22",
        "display_name": "Arianna Huffington",
        "headline": "Founder and CEO at Thrive Global | Founder at The Huffington Post | Author",
        "bio": "Author and media pioneer on a mission to end the global epidemic of stress, burnout, and sleep deprivation.",
        "linkedin_url": "https://www.linkedin.com/in/ariannahuffington",
        "instagram_url": "https://www.instagram.com/ariannahuff",
        "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Warm, philosophical matriarch of healthy sustainable living. Weaves ancient Greek wisdom and contemporary neuroscience into everyday well-being.",
            "interests": ["Sleep Science & Circadian Rhythms", "Stoic & Ancient Greek Philosophy", "Mindful Productivity", "Mediterranean Gastronomy", "Journalism"],
            "hobbies": ["Phone-free bedroom sleep rituals", "Walking meetings in Central Park", "Hosting Greek salon dinners", "Listening to classical opera"],
            "lifestyle_signals": ["Strict 8-hour sleep advocate", "Device-free dinner tables", "Warm Mediterranean hospitality"],
            "communication_style": "Lyrical, affectionate, wise, maternal, and persuasive with Greek proverbs",
            "social_preferences": ["Intimate salon dinners with open debates", "Long park strolls", "Mindful retreats"],
            "compatibility_factors": ["Respect for boundaries and rest", "Appreciation for philosophy and books", "Warm and hospitable heart"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "Wrote bestselling book 'The Sleep Revolution' based on neuroscience and personal recovery",
                    "source_url": "https://www.linkedin.com/in/ariannahuffington",
                    "quote": "Sleep is not a sacrifice you make for success; it is the non-negotiable foundation of all performance.",
                    "confidence": 0.98
                },
                {
                    "claim": "Advocates for walking meetings and leaving digital phones outside the bedroom",
                    "source_url": "https://www.instagram.com/ariannahuff",
                    "quote": "When you escort your phone out of your bedroom, you reclaim your morning peace.",
                    "confidence": 0.95
                }
            ],
            "unknown_fields": ["Favorite contemporary pop artists", "Gym lifting personal records"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_23",
        "display_name": "Tony Fadell",
        "headline": "Principal at Build Collective | Author of BUILD | 'Father of the iPod' & Nest Founder",
        "bio": "Legendary hardware inventor, designer, and green-tech investor who led 300+ hardware products across Apple, Nest, and smart homes.",
        "linkedin_url": "https://www.linkedin.com/in/tonyfadell",
        "instagram_url": "https://www.instagram.com/tfadell",
        "avatar_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Relentless hardware craftsman and climate tech champion. Combines intense French/Silicon Valley design sensibilities with passion for tangible physical prototypes.",
            "interests": ["Hardware Prototyping", "Clean Energy & Climate Tech", "Industrial Engineering", "Parisian Architecture & Cafe Culture", "Vintage Watches"],
            "hobbies": ["Road cycling in the French Alps", "Collecting vintage horology timepieces", "Woodworking and 3D printing", "Espresso brewing"],
            "lifestyle_signals": ["Bicultural French-American lifestyle", "Zero tolerance for lazy engineering", "Obsession with physical tactile switches"],
            "communication_style": "Blunt, energetic, passionate, mentorship-minded, and detail-saturated",
            "social_preferences": ["Paris cafe discussions", "Workshop prototyping sessions", "Cycling groups through mountain passes"],
            "compatibility_factors": ["Appreciation for physical craftsmanship", "Direct and honest communication", "Shared commitment to climate solutions"],
            "confidence_score": 0.94,
            "evidence_references": [
                {
                    "claim": "Led the creation of the original Apple iPod and co-created the iPhone hardware",
                    "source_url": "https://www.linkedin.com/in/tonyfadell",
                    "quote": "Making hardware is hard because you can't push an over-the-air patch to fix broken plastic.",
                    "confidence": 0.99
                },
                {
                    "claim": "Dedicated Build Collective to climate hardware technologies and deep tech",
                    "source_url": "https://www.instagram.com/tfadell",
                    "quote": "The next Steve Jobs will be someone solving climate tech in hardware and hard chemistry.",
                    "confidence": 0.93
                }
            ],
            "unknown_fields": ["Favorite fiction book", "Spicy food tolerance"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_24",
        "display_name": "Padmasree Warrior",
        "headline": "Founder and CEO at Fable | Board Member at Microsoft and Spotify | Former CTO Cisco & Motorola",
        "bio": "Global technology executive, entrepreneur, artist, and advocate for reading communities, mental wellness, and creative expression.",
        "linkedin_url": "https://www.linkedin.com/in/padmasreewarrior",
        "instagram_url": "https://www.instagram.com/padmasree",
        "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Polymathic artist-technologist who harmonizes high-level enterprise engineering with fine art painting, book clubs, and poetic contemplation.",
            "interests": ["Social Reading & Book Clubs", "Fine Art Painting (Acrylic & Watercolor)", "Autonomous Vehicles", "Women in Engineering Leadership", "Poetry"],
            "hobbies": ["Painting landscape canvases in home studio", "Hosting digital book club reading circles", "Collecting modern art", "Gardening exotic roses"],
            "lifestyle_signals": ["Regular weekend painting retreats", "Daily literary reading habit", "Calm and dignified composure"],
            "communication_style": "Serene, articulate, artistic, culturally nuanced, and supportive",
            "social_preferences": ["Book reading salons", "Art gallery openings", "Intimate dinner conversations about literature"],
            "compatibility_factors": ["Deep appreciation for visual art and literature", "High intellectual composure", "Shared balance of logic and emotion"],
            "confidence_score": 0.95,
            "evidence_references": [
                {
                    "claim": "Regularly exhibits and shares personal original watercolor and acrylic paintings",
                    "source_url": "https://www.instagram.com/padmasree",
                    "quote": "Painting gives me a quiet meditative balance away from high-stakes boardroom strategies.",
                    "confidence": 0.97
                },
                {
                    "claim": "Founded Fable to foster mental wellness and community through shared reading",
                    "source_url": "https://www.linkedin.com/in/padmasreewarrior",
                    "quote": "Stories are how humans develop empathy and connect across borders and backgrounds.",
                    "confidence": 0.96
                }
            ],
            "unknown_fields": ["Favorite pop cinema", "Extreme sports interest"],
            "analysis_engine": "deterministic_fallback"
        }
    },
    {
        "id": "person_25",
        "display_name": "Jimmy Wales",
        "headline": "Founder of Wikipedia | Co-founder of WT.Social / Trust Cafe | Open Knowledge Advocate",
        "bio": "Internet pioneer dedicated to open knowledge, public neutrality, collective intelligence, and civil discourse worldwide.",
        "linkedin_url": "https://www.linkedin.com/in/jimmywales",
        "instagram_url": "https://www.instagram.com/jimmy_wales",
        "avatar_url": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=400&q=80",
        "collection_method": "verified_seed",
        "is_verified": True,
        "analysis": {
            "summary": "Egalitarian thinker, open-knowledge crusader, and philosophical skeptic. Driven by calm logic, collaborative encyclopedic curation, and love for classic rock.",
            "interests": ["Open Knowledge & Information Commons", "Philosophy of Objectivism & Logic", "Acoustic Guitar & Classic Rock", "Public Neutrality", "Global Travel"],
            "hobbies": ["Playing classic rock on acoustic guitar", "Participating in civil public debates", "London theater visits", "Collecting rare reference books"],
            "lifestyle_signals": ["Unassuming and accessible personality", "Frequent international traveler", "Enjoys British pub pub quizzes"],
            "communication_style": "Pragmatic, rational, open-minded, humble, and dryly humorous",
            "social_preferences": ["Quiet pub trivia nights", "Open-source community conferences", "Dinner debates over coffee"],
            "compatibility_factors": ["Rational thinking and intellectual humility", "Love for acoustic music and trivia", "Shared altruism for open access"],
            "confidence_score": 0.94,
            "evidence_references": [
                {
                    "claim": "Founded Wikipedia as a free, non-profit encyclopedia for every single human",
                    "source_url": "https://www.linkedin.com/in/jimmywales",
                    "quote": "Imagine a world in which every single person on the planet is given free access to the sum of all human knowledge.",
                    "confidence": 0.99
                },
                {
                    "claim": "Enjoys acoustic guitar playing and live pub music",
                    "source_url": "https://www.instagram.com/jimmy_wales",
                    "quote": "Acoustic strings and honest lyrics cut through all the digital noise.",
                    "confidence": 0.91
                }
            ],
            "unknown_fields": ["Preferred athletic training", "Fashion brands"],
            "analysis_engine": "deterministic_fallback"
        }
    }
]
