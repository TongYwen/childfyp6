-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 25, 2025 at 12:01 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `child_growth_insights`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic_scores`
--

CREATE TABLE `academic_scores` (
  `id` int(11) NOT NULL,
  `child_id` int(11) NOT NULL,
  `subject` varchar(50) NOT NULL,
  `score` int(11) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `academic_scores`
--

INSERT INTO `academic_scores` (`id`, `child_id`, `subject`, `score`, `date`) VALUES
(11, 10, 'english', 85, '2022-04-01'),
(12, 10, 'math', 90, '2020-09-01'),
(13, 10, 'math', 50, '2025-05-01'),
(16, 12, 'math', 80, '2022-03-01'),
(17, 12, 'english', 60, '2022-03-01'),
(18, 12, 'bm', 70, '2022-03-01'),
(19, 12, 'math', 60, '2022-06-01'),
(20, 12, 'english', 50, '2022-06-01'),
(21, 12, 'bm', 40, '2022-06-01');

-- --------------------------------------------------------

--
-- Table structure for table `ai_results`
--

CREATE TABLE `ai_results` (
  `id` int(11) NOT NULL,
  `child_id` int(11) NOT NULL,
  `module` varchar(50) NOT NULL,
  `data` text DEFAULT NULL,
  `result` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `ai_results`
--

INSERT INTO `ai_results` (`id`, `child_id`, `module`, `data`, `result`, `created_at`, `updated_at`) VALUES
(1, 10, 'preschool', '[{\"id\": 10, \"child_id\": 10, \"domain\": \"Cognitive Milestones\", \"description\": \"observation\", \"date\": \"2025-11-01\", \"date_str\": \"2025-11\", \"age_months\": 34}, {\"id\": 11, \"child_id\": 10, \"domain\": \"Cognitive Milestones\", \"description\": \"observation\", \"date\": \"2025-11-01\", \"date_str\": \"2025-11\", \"age_months\": 34}, {\"id\": 12, \"child_id\": 10, \"domain\": \"Cognitive Milestones\", \"description\": \"observation\", \"date\": \"2025-11-01\", \"date_str\": \"2025-11\", \"age_months\": 34}, {\"id\": 4, \"child_id\": 10, \"domain\": \"Social/Emotional Milestones\", \"description\": \"ASSESSMENT\", \"date\": \"2025-10-01\", \"date_str\": \"2025-10\", \"age_months\": 33}]', 'The child, mee, born on 2023-01-02, is approximately 34 months (2 years, 10 months) old at the time of the last recorded milestone.\n\n<p><h3>Age-appropriate Areas:</h3></p>\n<p>The recorded milestones, \"Cognitive Milestones: observation (at 34 months)\" and \"Social/Emotional Milestones: ASSESSMENT (at 33 months),\" are too broad and general to allow for a specific comparison to the detailed, observable benchmarks provided. If \"observation\" indicates a general capacity for cognitive engagement and \"ASSESSMENT\" implies a satisfactory review of social-emotional skills, then these broad domains might be considered age-appropriate. However, without specific examples of what \'observation\' entails or the outcomes of the \'ASSESSMENT,\' it is difficult to confirm age-appropriateness against the granular standard milestones for a 34-month-old child, who is expected to be developing skills such as showing simple problem-solving, pretending with objects, following two-step instructions, and engaging in conversations.</p>\n\n<p><h3>Delayed Areas:</h3></p>\n<p>Given the highly generalized nature of the child\'s recorded milestones, it is not possible to identify specific areas of delay. If \'observation\' were to refer to very basic visual tracking or attention, this would be significantly delayed as such skills are typically achieved in early infancy (e.g., \'Looks at your face\' at 2 months). However, it is more likely that \'observation\' is intended as a general statement of cognitive function rather than a specific, new skill.</p>\n\n<p><h3>Advanced Areas:</h3></p>\n<p>Due to the lack of specific detail in the recorded milestones, no advanced developmental areas can be definitively identified. The general terms \'observation\' and \'ASSESSMENT\' do not provide sufficient information to determine if mee is exceeding typical developmental expectations in any domain.</p>\n\n<p>Overall, the child\'s recorded milestones are too vague to provide a detailed comparison with standard age-based benchmarks, limiting the ability to precisely assess specific areas of development.</p>', '2025-10-09 15:22:44', '2025-10-13 15:55:13'),
(2, 10, 'learning', '{\n  \"observations\": [\n    {\n      \"id\": 4,\n      \"child_id\": 10,\n      \"observation\": \"ABC\",\n      \"created_at\": \"2025-10-09 23:25:04\"\n    }\n  ],\n  \"answers\": []\n}', '<p><strong>Most Likely Learning Style:</strong> Mixed (Visual, Auditory, and Kinesthetic)</p>\n\n<h3>Reasoning:</h3>\n<p>\n    Given the very limited observation of \"ABC\" and the absence of specific test responses, it is most probable that this preschooler demonstrates a Mixed learning style, engaging multiple senses. In early childhood, foundational knowledge like the alphabet is typically acquired through a combination of visual input (seeing letters in books or on charts), auditory engagement (singing alphabet songs or hearing letter sounds), and kinesthetic activities (tracing letters, manipulating alphabet blocks, or using actions for letter recognition). Without more detailed behavioral observations or specific indicators of preference, a multi-modal approach is generally the most effective and common learning pathway for young children to absorb and process new information.\n</p>\n\n<h3>Actionable Suggestions for Parents/Teachers:</h3>\n<ul>\n    <li><strong>Utilize Multi-Sensory Activities:</strong> Integrate sight, sound, and touch into learning. For example, use colorful alphabet flashcards (visual), sing the ABC song (auditory), and encourage tracing letters in sand or with play-doh (kinesthetic).</li>\n    <li><strong>Observe and Adapt:</strong> Pay close attention to which activities the child seems most engaged with or responds to best. This ongoing observation can help identify emerging preferences and allow for further customization of learning experiences.</li>\n    <li><strong>Incorporate Hands-On Exploration:</strong> Provide plenty of opportunities for active, discovery-based learning. Building with letter blocks, playing alphabet puzzles, and engaging in movement-based games are excellent ways to reinforce concepts.</li>\n    <li><strong>Read Aloud and Use Rhymes:</strong> Regularly read picture books, point out letters and words, and recite nursery rhymes or songs. This strengthens both visual and auditory processing skills, fostering early literacy development.</li>\n    <li><strong>Create a Varied Learning Environment:</strong> Offer a mix of structured and free-play activities, both indoors and outdoors, to cater to different energy levels and provide diverse opportunities for learning and exploration.</li>\n</ul>', '2025-10-09 15:25:31', '2025-10-09 15:25:31'),
(3, 10, 'tutoring', '{\n  \"learning\": \"<p><strong>Most Likely Learning Style:</strong> Mixed (Visual, Auditory, and Kinesthetic)</p>\\n\\n<h3>Reasoning:</h3>\\n<p>\\n    Given the very limited observation of \\\"ABC\\\" and the absence of specific test responses, it is most probable that this preschooler demonstrates a Mixed learning style, engaging multiple senses. In early childhood, foundational knowledge like the alphabet is typically acquired through a combination of visual input (seeing letters in books or on charts), auditory engagement (singing alphabet songs or hearing letter sounds), and kinesthetic activities (tracing letters, manipulating alphabet blocks, or using actions for letter recognition). Without more detailed behavioral observations or specific indicators of preference, a multi-modal approach is generally the most effective and common learning pathway for young children to absorb and process new information.\\n</p>\\n\\n<h3>Actionable Suggestions for Parents/Teachers:</h3>\\n<ul>\\n    <li><strong>Utilize Multi-Sensory Activities:</strong> Integrate sight, sound, and touch into learning. For example, use colorful alphabet flashcards (visual), sing the ABC song (auditory), and encourage tracing letters in sand or with play-doh (kinesthetic).</li>\\n    <li><strong>Observe and Adapt:</strong> Pay close attention to which activities the child seems most engaged with or responds to best. This ongoing observation can help identify emerging preferences and allow for further customization of learning experiences.</li>\\n    <li><strong>Incorporate Hands-On Exploration:</strong> Provide plenty of opportunities for active, discovery-based learning. Building with letter blocks, playing alphabet puzzles, and engaging in movement-based games are excellent ways to reinforce concepts.</li>\\n    <li><strong>Read Aloud and Use Rhymes:</strong> Regularly read picture books, point out letters and words, and recite nursery rhymes or songs. This strengthens both visual and auditory processing skills, fostering early literacy development.</li>\\n    <li><strong>Create a Varied Learning Environment:</strong> Offer a mix of structured and free-play activities, both indoors and outdoors, to cater to different energy levels and provide diverse opportunities for learning and exploration.</li>\\n</ul>\",\n  \"preschool\": \"The child, mee, born on 2023-01-02, is approximately 34 months (2 years, 10 months) old at the time of the last recorded milestone.\\n\\n<p><h3>Age-appropriate Areas:</h3></p>\\n<p>The recorded milestones, \\\"Cognitive Milestones: observation (at 34 months)\\\" and \\\"Social/Emotional Milestones: ASSESSMENT (at 33 months),\\\" are too broad and general to allow for a specific comparison to the detailed, observable benchmarks provided. If \\\"observation\\\" indicates a general capacity for cognitive engagement and \\\"ASSESSMENT\\\" implies a satisfactory review of social-emotional skills, then these broad domains might be considered age-appropriate. However, without specific examples of what \'observation\' entails or the outcomes of the \'ASSESSMENT,\' it is difficult to confirm age-appropriateness against the granular standard milestones for a 34-month-old child, who is expected to be developing skills such as showing simple problem-solving, pretending with objects, following two-step instructions, and engaging in conversations.</p>\\n\\n<p><h3>Delayed Areas:</h3></p>\\n<p>Given the highly generalized nature of the child\'s recorded milestones, it is not possible to identify specific areas of delay. If \'observation\' were to refer to very basic visual tracking or attention, this would be significantly delayed as such skills are typically achieved in early infancy (e.g., \'Looks at your face\' at 2 months). However, it is more likely that \'observation\' is intended as a general statement of cognitive function rather than a specific, new skill.</p>\\n\\n<p><h3>Advanced Areas:</h3></p>\\n<p>Due to the lack of specific detail in the recorded milestones, no advanced developmental areas can be definitively identified. The general terms \'observation\' and \'ASSESSMENT\' do not provide sufficient information to determine if mee is exceeding typical developmental expectations in any domain.</p>\\n\\n<p>Overall, the child\'s recorded milestones are too vague to provide a detailed comparison with standard age-based benchmarks, limiting the ability to precisely assess specific areas of development.</p>\"\n}', '<h3>1. Potential Weak Areas or Skills that May Need Support:</h3>\n<ul>\n    <li>**Lack of Specific Developmental Data:** The most significant area needing support is the absence of detailed, observable milestones across all key developmental domains (Cognitive, Language, Fine Motor, Gross Motor, Social-Emotional). Without this specific information, it is impossible to accurately identify Mee\'s unique strengths or precise areas requiring targeted support relative to age-appropriate benchmarks for a 34-month-old.</li>\n    <li>**Undefined Cognitive Skills:** While \"observation\" is noted, specific cognitive abilities expected at 34 months, such as simple problem-solving, understanding of basic concepts (e.g., shapes, colors, numbers), memory, and engaging in pretend play, are not documented. These areas may require support if not adequately developed.</li>\n    <li>**Undefined Language and Communication Skills:** There is no recorded information regarding Mee\'s expressive or receptive language, vocabulary size, ability to follow two-step instructions, or engagement in back-and-forth conversations. These are critical developmental markers at this age and represent potential areas of needed focus.</li>\n    <li>**Undefined Fine and Gross Motor Skills:** Essential physical development areas like manipulating small objects, pre-writing skills, drawing, running, jumping, and balancing are not mentioned, leaving these domains unassessed and potentially in need of targeted activities.</li>\n    <li>**Undefined Social-Emotional Specifics:** While an \"ASSESSMENT\" was completed, the specifics of Mee\'s social interactions (e.g., sharing, turn-taking), emotional regulation, independence in self-care, or imaginative play skills are unknown.</li>\n</ul>\n\n<h3>2. Subjects or Developmental Domains Where Tutoring or Extra Help Would Be Most Beneficial:</h3>\n<ul>\n    <li>**Comprehensive Developmental Assessment:** The most crucial initial \"extra help\" would be a thorough, detailed assessment across all developmental domains (Cognitive, Language, Social-Emotional, Fine Motor, Gross Motor). This would establish a baseline, identify specific strengths, and pinpoint precise areas requiring targeted intervention or support.</li>\n    <li>**Early Literacy and Language Development:** Given the mention of \"ABC\" and the critical importance of language at this age, support in vocabulary expansion, listening comprehension, following instructions, engaging in simple conversations, letter recognition, and pre-reading skills would be highly beneficial.</li>\n    <li>**Foundational Cognitive Skills:** Tutoring could focus on problem-solving through puzzles and games, sorting and matching activities, understanding basic concepts (colors, shapes, numbers), and developing memory skills through engaging play.</li>\n    <li>**Social-Emotional Skill Building:** Opportunities for structured and unstructured social play to develop skills such as sharing, turn-taking, empathy, and appropriate emotional expression.</li>\n    <li>**Fine and Gross Motor Coordination:** Activities designed to enhance hand-eye coordination (e.g., stacking, threading), pre-writing skills (e.g., tracing, scribbling), balance, and overall physical agility through active play.</li>\n</ul>\n\n<h3>3. Personalized Activity or Tutoring Style Recommendations Aligned with the Learning Style:</h3>\n<ul>\n    <li>**Multi-Sensory Play-Based Learning:** Since Mee exhibits a Mixed (Visual, Auditory, Kinesthetic) learning style, all learning should be embedded in play and actively engage multiple senses simultaneously. For example, when learning about animals, use picture cards (visual), make animal sounds (auditory), and pretend to be the animals (kinesthetic).</li>\n    <li>**Hands-On Exploration and Discovery:** Provide abundant opportunities for Mee to manipulate objects, build, trace, and engage in active, discovery-based learning. Examples include using alphabet blocks, play-doh for letter formation, sensory bins, science experiments for toddlers, and movement-based games to learn concepts.</li>\n    <li>**Visual Reinforcement:** Utilize colorful picture books, flashcards, charts, and visual schedules to aid understanding and memory. Point to letters, words, and objects while talking about them to connect visual cues with auditory information. Demonstrations are also highly effective.</li>\n    <li>**Auditory Engagement through Storytelling and Music:** Incorporate reading aloud daily, singing songs (especially alphabet, number, and concept-based songs), reciting rhymes, and engaging in verbal storytelling. Encourage Mee to repeat words, phrases, and sounds to build vocabulary and listening skills.</li>\n    <li>**Interactive and Conversational Approach:** Foster active participation by asking open-ended questions (\"What do you think will happen next?\"), responding to Mee\'s queries with enthusiasm, and creating a dialogue-rich environment to develop language and critical thinking.</li>\n    <li>**Varied Activities and Environments:** Offer a diverse range of activities, alternating between quiet indoor tasks (e.g., drawing, puzzles) and active outdoor play (e.g., running, climbing), and switching between structured learning and free exploration to maintain engagement and cater to different aspects of the mixed learning style.</li>\n</ul>\n\nFor parents and teachers, the immediate priority is to conduct a detailed and specific assessment of Mee\'s development across all key domains. This comprehensive understanding will allow for the implementation of highly personalized, multi-sensory, and play-based learning experiences that leverage Mee\'s mixed learning style to support optimal growth in language, cognitive, social, and motor skills.', '2025-10-09 15:26:30', '2025-10-16 15:22:35'),
(11, 11, 'learning', '{\n  \"observations\": [\n    {\n      \"id\": 8,\n      \"child_id\": 11,\n      \"observation\": \"hand on activities\",\n      \"created_at\": \"2025-10-17 14:23:48\"\n    }\n  ],\n  \"answers\": [\n    {\n      \"answer_id\": 7,\n      \"test_id\": 4,\n      \"question_id\": 22,\n      \"answer\": \"2\",\n      \"created_at\": \"2025-10-16 23:29:52\",\n      \"test_name\": \"abc\",\n      \"question_text\": \"1+1\"\n    },\n    {\n      \"answer_id\": 8,\n      \"test_id\": 4,\n      \"question_id\": 23,\n      \"answer\": \"3\",\n      \"created_at\": \"2025-10-16 23:29:52\",\n      \"test_name\": \"abc\",\n      \"question_text\": \"2+2\"\n    },\n    {\n      \"answer_id\": 9,\n      \"test_id\": 4,\n      \"question_id\": 24,\n      \"answer\": \"5\",\n      \"created_at\": \"2025-10-16 23:29:52\",\n      \"test_name\": \"abc\",\n      \"question_text\": \"3+2\"\n    }\n  ]\n}', '<div style=\"font-family: Arial, sans-serif; line-height: 1.6;\">\n\n    <h2 style=\"color: #2c3e50;\">Learning Style Assessment</h2>\n\n    <p style=\"font-size: 1.1em;\">\n        Based on the observations and test responses, this child\'s most likely learning style is <strong style=\"color: #27ae60;\">Kinesthetic</strong>.\n    </p>\n\n    <h3 style=\"color: #2c3e50;\">Reasoning:</h3>\n    <p>\n        The key observation, \"hand on activities,\" strongly suggests that this child learns best by doing, touching, and experiencing. Kinesthetic learners thrive when they can actively engage with materials and concepts through movement and physical manipulation. They often understand and remember information more effectively when it\'s connected to a tangible experience rather than just seeing or hearing it. This active, exploratory approach is crucial for their cognitive development and engagement in learning tasks.\n    </p>\n\n    <h3 style=\"color: #2c3e50;\">Actionable Suggestions for Parents and Teachers:</h3>\n    <ul style=\"list-style-type: disc; margin-left: 20px;\">\n        <li style=\"margin-bottom: 8px;\">\n            <strong style=\"color: #3498db;\">Incorporate Movement:</strong> Use physical games like jumping to numbers, acting out stories, or building with blocks to teach new concepts.\n        </li>\n        <li style=\"margin-bottom: 8px;\">\n            <strong style=\"color: #3498db;\">Provide Manipulatives:</strong> Offer a variety of hands-on tools such as counters, puzzles, play-dough, or sensory bins for exploring math, letters, and scientific ideas.\n        </li>\n        <li style=\"margin-bottom: 8px;\">\n            <strong style=\"color: #3498db;\">Encourage Practical Exploration:</strong> Involve the child in real-world tasks like helping with cooking (measuring ingredients), gardening (planting seeds), or sorting laundry to make learning relevant and tactile.\n        </li>\n        <li style=\"margin-bottom: 8px;\">\n            <strong style=\"color: #3498db;\">Create Learning Stations:</strong> Design activity zones where they can build, experiment, and engage with different textures and materials, allowing them to discover at their own pace.\n        </li>\n    </ul>\n\n</div>', '2025-10-16 15:30:22', '2025-10-17 06:25:00'),
(12, 11, 'tutoring', '{\n  \"learning\": \"<div style=\\\"font-family: Arial, sans-serif; line-height: 1.6;\\\">\\n\\n    <h2 style=\\\"color: #2c3e50;\\\">Learning Style Assessment</h2>\\n\\n    <p style=\\\"font-size: 1.1em;\\\">\\n        Based on the observations and test responses, this child\'s most likely learning style is <strong style=\\\"color: #27ae60;\\\">Kinesthetic</strong>.\\n    </p>\\n\\n    <h3 style=\\\"color: #2c3e50;\\\">Reasoning:</h3>\\n    <p>\\n        The key observation, \\\"hand on activities,\\\" strongly suggests that this child learns best by doing, touching, and experiencing. Kinesthetic learners thrive when they can actively engage with materials and concepts through movement and physical manipulation. They often understand and remember information more effectively when it\'s connected to a tangible experience rather than just seeing or hearing it. This active, exploratory approach is crucial for their cognitive development and engagement in learning tasks.\\n    </p>\\n\\n    <h3 style=\\\"color: #2c3e50;\\\">Actionable Suggestions for Parents and Teachers:</h3>\\n    <ul style=\\\"list-style-type: disc; margin-left: 20px;\\\">\\n        <li style=\\\"margin-bottom: 8px;\\\">\\n            <strong style=\\\"color: #3498db;\\\">Incorporate Movement:</strong> Use physical games like jumping to numbers, acting out stories, or building with blocks to teach new concepts.\\n        </li>\\n        <li style=\\\"margin-bottom: 8px;\\\">\\n            <strong style=\\\"color: #3498db;\\\">Provide Manipulatives:</strong> Offer a variety of hands-on tools such as counters, puzzles, play-dough, or sensory bins for exploring math, letters, and scientific ideas.\\n        </li>\\n        <li style=\\\"margin-bottom: 8px;\\\">\\n            <strong style=\\\"color: #3498db;\\\">Encourage Practical Exploration:</strong> Involve the child in real-world tasks like helping with cooking (measuring ingredients), gardening (planting seeds), or sorting laundry to make learning relevant and tactile.\\n        </li>\\n        <li style=\\\"margin-bottom: 8px;\\\">\\n            <strong style=\\\"color: #3498db;\\\">Create Learning Stations:</strong> Design activity zones where they can build, experiment, and engage with different textures and materials, allowing them to discover at their own pace.\\n        </li>\\n    </ul>\\n\\n</div>\",\n  \"preschool\": null\n}', '<div style=\"font-family: Arial, sans-serif; line-height: 1.6;\">\n\n    <h2 style=\"color: #2c3e50;\">Tutoring and Support Recommendations for a Kinesthetic Learner</h2>\n\n    <p style=\"font-size: 1.1em;\">\n        Based on the provided learning style analysis, which identifies the child as a primary kinesthetic learner, the following recommendations are tailored to support their unique developmental needs. Kinesthetic learners thrive through movement, touch, and hands-on interaction, meaning their educational experiences should be rich with physical engagement.\n    </p>\n\n    <h3 style=\"color: #2c3e50;\">1. Potential Weak Areas or Skills That May Need Support:</h3>\n    <ul>\n        <li><strong>Abstract Concepts:</strong> Without concrete, hands-on examples, this child may struggle to grasp abstract ideas in subjects like early math (e.g., addition without counters) or language arts (e.g., understanding a story purely through listening).</li>\n        <li><strong>Sustained Passive Learning:</strong> Activities requiring long periods of sitting still, listening, or simply observing (e.g., extended story times without interactive elements, flashcard drills without physical manipulation) may lead to disengagement, difficulty focusing, or appearing restless.</li>\n        <li><strong>Rote Memorization:</strong> Learning facts, letters, or numbers without a physical or experiential connection (e.g., tracing letters, building number towers) might be less effective and require more effort than for other learning styles.</li>\n        <li><strong>Fine Motor Skill Development (if not actively engaged):</strong> While kinesthetic learners often enjoy fine motor activities, if the learning environment doesn\'t offer ample opportunities for manipulation (e.g., puzzles, play-dough, cutting, drawing), these skills might not be fully developed in a way that aligns with their learning style.</li>\n    </ul>\n\n    <h3 style=\"color: #2c3e50;\">2. Subjects or Developmental Domains Where Tutoring or Extra Help Would Be Most Beneficial:</h3>\n    <ul>\n        <li><strong>Early Literacy (Letters, Sounds, Story Comprehension):</strong> Tutoring could focus on tracing letters in sand, building letters with blocks, acting out story characters, or using magnetic letters to form words, making reading and writing foundational skills tangible.</li>\n        <li><strong>Early Numeracy (Counting, Number Recognition, Basic Math Concepts):</strong> Extra support using counters, building blocks for addition/subtraction, sorting objects by attributes, or physical games that involve counting and measuring would be highly effective.</li>\n        <li><strong>Science and Exploration:</strong> Hands-on experiments, nature walks with active collection and observation, and building simple machines or models would deepen understanding.</li>\n        <li><strong>Problem-Solving and Critical Thinking:</strong> Tutoring through puzzles, construction tasks, and experimental play allows the child to physically manipulate elements to discover solutions.</li>\n    </ul>\n\n    <h3 style=\"color: #2c3e50;\">3. Personalized Activity or Tutoring Style Recommendations:</h3>\n    <ul>\n        <li><strong>Active Learning Sessions:</strong> Tutoring should incorporate frequent movement breaks and integrate physical activity directly into lessons. For example, jumping jacks for each correct answer, or moving around to find \"hidden\" sight words.</li>\n        <li><strong>Manipulatives are Key:</strong> Always have a variety of hands-on tools available. This includes blocks, counters, sensory bins (rice, beans, water beads) for letter/number recognition, play-dough for letter formation, and tangrams for spatial reasoning.</li>\n        <li><strong>Experiential and Practical Tasks:</strong> Frame learning within real-world scenarios. For example, use cooking to teach measurement, gardening to understand plant cycles, or sorting laundry to practice classification and counting.</li>\n        <li><strong>Building and Constructing:</strong> Incorporate building tasks related to concepts. If learning about shapes, build structures using those shapes. If learning about animals, build animal enclosures.</li>\n        <li><strong>Role-Playing and Acting Out:</strong> For stories or social-emotional learning, encourage the child to act out scenarios or become characters. This helps them embody the learning.</li>\n        <li><strong>Sensory Engagement:</strong> Utilize multiple senses. Beyond touch, consider textures, smells, and even tastes (safely) when appropriate to create a multi-sensory learning experience.</li>\n    </ul>\n\n    <p style=\"font-size: 1.1em;\">\n        For parents and teachers, understanding this child\'s kinesthetic learning style is crucial for fostering engagement and effective learning. By prioritizing movement, hands-on activities, and practical exploration across all subjects, you can create an enriching environment where this child feels understood, thrives, and builds a strong foundation for future academic success. The goal is to make learning an active, physical adventure rather than a passive observation.\n    </p>\n\n</div>', '2025-10-16 15:33:36', '2025-10-17 10:26:21'),
(13, 12, 'preschool', '[{\"id\": 14, \"child_id\": 12, \"domain\": \"Language/Communication\", \"description\": \"test\", \"date\": \"2025-11-01\", \"date_str\": \"2025-11\", \"age_months\": 68}, {\"id\": 15, \"child_id\": 12, \"domain\": \"Movement/Physical Development\", \"description\": \"My child do not know how to walk even she is 5 years old\", \"date\": \"2025-11-01\", \"date_str\": \"2025-11\", \"age_months\": 68}, {\"id\": 16, \"child_id\": 12, \"domain\": \"Social/Emotional Milestones\", \"description\": \"Always not happy\", \"date\": \"2025-11-01\", \"date_str\": \"2025-11\", \"age_months\": 68}]', '<div style=\"font-family: Arial, sans-serif;\">\n    <p><strong>Child\'s Age for Assessment:</strong> 68 months (5 years and 8 months)</p>\n\n    <h3 style=\"color: #4CAF50;\">Areas that are age-appropriate</h3>\n    <ul>\n        <li>No specific milestones were recorded as age-appropriate for Lam Ah Li at 68 months based on the provided data.</li>\n    </ul>\n\n    <h3 style=\"color: #F44336;\">Areas that are delayed</h3>\n    <ul>\n        <li><strong>Movement/Physical Development:</strong> Lam Ah Li does not know how to walk at 68 months (5 years 8 months). Independent walking is typically achieved by 18 months. This represents a severe developmental delay in this area.</li>\n        <li><strong>Social/Emotional Milestones:</strong> Lam Ah Li is recorded as \"Always not happy\" at 68 months. Typical social-emotional development for a child of this age includes expressing a range of emotions, engaging happily with others, and showing empathy. This observation suggests significant concerns regarding emotional well-being and social-emotional development.</li>\n        <li><strong>Language/Communication:</strong> Although a \"test\" was recorded, no specific language achievements (e.g., telling stories, speaking in complex sentences, naming letters) are provided for Lam Ah Li at 68 months. For a child of this age, significant progress in verbal communication is expected. The absence of reported milestones suggests a likely delay in this area.</li>\n    </ul>\n\n    <h3 style=\"color: #2196F3;\">Areas that are advanced for the child\'s age</h3>\n    <ul>\n        <li>No advanced milestones were recorded for Lam Ah Li based on the provided data.</li>\n    </ul>\n\n    <p style=\"font-weight: bold; margin-top: 20px;\">\n        Overall, Lam Ah Li demonstrates significant developmental delays in Movement/Physical Development and Social/Emotional Milestones, with concerns regarding Language/Communication based on the absence of reported age-appropriate achievements.\n    </p>\n</div>', '2025-11-19 04:36:26', '2025-11-19 17:06:45'),
(14, 12, 'tutoring', '{\n  \"learning\": \"<p><strong>Most Likely Learning Style:</strong> Kinesthetic</p>\\n\\n<p>\\n    Based on the observation that the child \\\"cannot focus while study and learning at school,\\\" a kinesthetic learning style is the most likely.\\n    Kinesthetic learners thrive when they can move, touch, and interact physically with their learning environment to process information.\\n    Traditional classroom settings, which often require children to sit still for extended periods, can be particularly challenging for these active learners, leading to apparent difficulties with focus and attention.\\n    Their inherent need for movement and hands-on engagement is central to how they process and retain new information effectively.\\n</p>\\n\\n<h3>Actionable Suggestions:</h3>\\n<ul>\\n    <li>Integrate physical activity into lessons, such as movement breaks, standing desks, or learning games that involve gross motor skills.</li>\\n    <li>Provide hands-on learning opportunities using manipulatives, playdough, blocks, or other tactile materials to explore concepts.</li>\\n    <li>Encourage role-playing, experiments, and building activities where the child can actively participate and experience the learning content.</li>\\n    <li>Allow for frequent, short breaks where the child can stand up, stretch, or move around to help regulate their energy and attention.</li>\\n    <li>Utilize sensory bins or textured objects during quiet time activities to engage their tactile senses in a focused way.</li>\\n</ul>\",\n  \"preschool\": \"<div style=\\\"font-family: Arial, sans-serif;\\\">\\n    <p><strong>Child\'s Age for Assessment:</strong> 68 months (5 years and 8 months)</p>\\n\\n    <h3 style=\\\"color: #4CAF50;\\\">Areas that are age-appropriate</h3>\\n    <ul>\\n        <li>No specific milestones were recorded as age-appropriate for Lam Ah Li at 68 months based on the provided data.</li>\\n    </ul>\\n\\n    <h3 style=\\\"color: #F44336;\\\">Areas that are delayed</h3>\\n    <ul>\\n        <li><strong>Movement/Physical Development:</strong> Lam Ah Li does not know how to walk at 68 months (5 years 8 months). Independent walking is typically achieved by 18 months. This represents a severe developmental delay in this area.</li>\\n        <li><strong>Social/Emotional Milestones:</strong> Lam Ah Li is recorded as \\\"Always not happy\\\" at 68 months. Typical social-emotional development for a child of this age includes expressing a range of emotions, engaging happily with others, and showing empathy. This observation suggests significant concerns regarding emotional well-being and social-emotional development.</li>\\n        <li><strong>Language/Communication:</strong> Although a \\\"test\\\" was recorded, no specific language achievements (e.g., telling stories, speaking in complex sentences, naming letters) are provided for Lam Ah Li at 68 months. For a child of this age, significant progress in verbal communication is expected. The absence of reported milestones suggests a likely delay in this area.</li>\\n    </ul>\\n\\n    <h3 style=\\\"color: #2196F3;\\\">Areas that are advanced for the child\'s age</h3>\\n    <ul>\\n        <li>No advanced milestones were recorded for Lam Ah Li based on the provided data.</li>\\n    </ul>\\n\\n    <p style=\\\"font-weight: bold; margin-top: 20px;\\\">\\n        Overall, Lam Ah Li demonstrates significant developmental delays in Movement/Physical Development and Social/Emotional Milestones, with concerns regarding Language/Communication based on the absence of reported age-appropriate achievements.\\n    </p>\\n</div>\"\n}', '<h3>1. Potential Weak Areas or Skills Needing Support</h3>\n<ul>\n    <li><strong>Gross Motor Skills:</strong> Severe delay in walking and overall physical coordination.</li>\n    <li><strong>Fine Motor Skills:</strong> Likely impacted due to overall motor development delays, affecting tasks requiring dexterity.</li>\n    <li><strong>Emotional Regulation and Expression:</strong> Difficulty managing and communicating emotions, indicated by \"always not happy.\"</li>\n    <li><strong>Social Engagement and Interaction:</strong> Challenges in connecting with peers and participating in social play, stemming from emotional well-being concerns.</li>\n    <li><strong>Receptive and Expressive Language:</strong> Understanding spoken language and verbally communicating thoughts, needs, and ideas.</li>\n    <li><strong>Attention and Focus:</strong> Difficulty sustaining concentration, potentially linked to her kinesthetic learning style not being met and/or underlying developmental factors.</li>\n    <li><strong>Adaptive Skills:</strong> Basic self-care and daily living activities may be impacted by physical and cognitive delays.</li>\n    <li><strong>Overall Cognitive Development:</strong> The presence of multiple severe delays suggests a need for comprehensive assessment and support in foundational cognitive areas.</li>\n</ul>\n\n<h3>2. Subjects or Developmental Domains for Tutoring/Extra Help</h3>\n<ul>\n    <li><strong>Physical Therapy (PT):</strong> Absolutely essential to address the severe delay in walking, improve balance, coordination, and overall gross motor development.</li>\n    <li><strong>Occupational Therapy (OT):</strong> Highly beneficial for sensory integration, developing fine motor skills, enhancing body awareness, and supporting adaptive daily living skills.</li>\n    <li><strong>Speech and Language Therapy (SLT):</strong> Critical for fostering both receptive language (understanding speech) and expressive language (verbal communication, vocabulary, sentence formation).</li>\n    <li><strong>Developmental Play Therapy / Emotional Support:</strong> To address the \"always not happy\" observation, help her understand and express emotions, develop coping strategies, and foster positive social interactions.</li>\n    <li><strong>Early Childhood Special Education Services:</strong> A comprehensive, integrated approach focusing on all developmental domains (cognitive, social-emotional, communication, physical) with individualized educational plans.</li>\n    <li><strong>Behavioral Support:</strong> To help manage any challenging behaviors that may arise from frustration or communication difficulties, and to teach positive behavioral strategies.</li>\n</ul>\n\n<h3>3. Personalized Activity and Tutoring Style Recommendations</h3>\n<ul>\n    <li><strong>Movement-Integrated Learning:</strong> Embed physical activity into all learning tasks. For example, use action songs for language development, create obstacle courses that require following multi-step directions, or incorporate movement breaks every 10-15 minutes.</li>\n    <li><strong>Hands-on and Experiential Learning:</strong> Utilize manipulatives for learning concepts (e.g., blocks for math, playdough for letter formation), sensory bins for tactile exploration (e.g., finding letters in sand), and real-life experiences (e.g., helping in the kitchen, gardening) to build vocabulary and understanding.</li>\n    <li><strong>Role-Playing and Pretend Play:</strong> Encourage dramatic play scenarios to practice social skills, emotional expression, and language in a dynamic, engaging way. Use puppets or dress-up clothes.</li>\n    <li><strong>Active Games and Adaptive Sports:</strong> Introduce games that are adaptable to her physical abilities to encourage participation, motor skill development, and social interaction in a fun context.</li>\n    <li><strong>Short, Focused Sessions with Frequent Breaks:</strong> Structure learning into brief, intensive bursts (5-10 minutes) followed by active movement breaks or sensory input to help regulate attention and energy.</li>\n    <li><strong>Multi-Sensory Approaches:</strong> Always combine visual, auditory, and kinesthetic inputs. For example, when learning new words, say the word, show a picture, and have her act it out or touch a related object.</li>\n    <li><strong>Positive Reinforcement and Scaffolding:</strong> Provide abundant praise and positive feedback for effort and small achievements. Break down tasks into very small, manageable steps, providing hands-on assistance and gradually reducing support as she gains mastery.</li>\n    <li><strong>Use of Visual Schedules and Timers:</strong> To help manage transitions and expectations, particularly when incorporating movement breaks, as kinesthetic learners can sometimes struggle with transitions.</li>\n</ul>\n\n<p><strong>Summary for Parents or Teachers:</strong><br>\nLam Ah Li requires a comprehensive and highly individualized support plan that prioritizes addressing her significant developmental delays across physical, social-emotional, and language domains. Given her strong kinesthetic learning style, all interventions and learning opportunities should be exceptionally active, hands-on, and engaging. Consistent collaboration with specialized therapists (Physical, Occupational, and Speech-Language) is crucial, alongside an educational approach that integrates movement, experiential learning, and sensory input into every aspect of her day. A nurturing, patient, and stimulating environment will be key to fostering her development and overall well-being.</p>', '2025-11-19 04:37:00', '2025-11-19 17:07:53'),
(15, 12, 'learning', '{\n  \"observations\": [\n    {\n      \"id\": 9,\n      \"child_id\": 12,\n      \"observation\": \"Cannot focus while study and learning at school\",\n      \"created_at\": \"2025-11-19 12:39:17\"\n    }\n  ],\n  \"answers\": []\n}', '<p><strong>Most Likely Learning Style:</strong> Kinesthetic</p>\n\n<p>\n    Based on the observation that the child \"cannot focus while study and learning at school,\" a kinesthetic learning style is the most likely.\n    Kinesthetic learners thrive when they can move, touch, and interact physically with their learning environment to process information.\n    Traditional classroom settings, which often require children to sit still for extended periods, can be particularly challenging for these active learners, leading to apparent difficulties with focus and attention.\n    Their inherent need for movement and hands-on engagement is central to how they process and retain new information effectively.\n</p>\n\n<h3>Actionable Suggestions:</h3>\n<ul>\n    <li>Integrate physical activity into lessons, such as movement breaks, standing desks, or learning games that involve gross motor skills.</li>\n    <li>Provide hands-on learning opportunities using manipulatives, playdough, blocks, or other tactile materials to explore concepts.</li>\n    <li>Encourage role-playing, experiments, and building activities where the child can actively participate and experience the learning content.</li>\n    <li>Allow for frequent, short breaks where the child can stand up, stretch, or move around to help regulate their energy and attention.</li>\n    <li>Utilize sensory bins or textured objects during quiet time activities to engage their tactile senses in a focused way.</li>\n</ul>', '2025-11-19 04:39:25', '2025-11-19 04:39:25'),
(16, 12, 'insights', '{\"scores\": [{\"subject\": \"math\", \"score\": 80, \"date\": \"2022-03-01\"}, {\"subject\": \"english\", \"score\": 60, \"date\": \"2022-03-01\"}, {\"subject\": \"bm\", \"score\": 70, \"date\": \"2022-03-01\"}, {\"subject\": \"math\", \"score\": 60, \"date\": \"2022-06-01\"}, {\"subject\": \"english\", \"score\": 50, \"date\": \"2022-06-01\"}, {\"subject\": \"bm\", \"score\": 40, \"date\": \"2022-06-01\"}]}', 'Dear Lam Ah Li\'s Parents,\n\nIt\'s wonderful to see Lam Ah Li\'s learning journey unfold at age 5! Based on recent observations, Ah Li is showing some lovely strengths and areas where we can nurture even more growth. We\'ve noticed Ah Li demonstrates a good grasp of early math concepts, often showing a solid understanding in this area.\n\nWe also see that Ah Li is developing well in English, and there are some wonderful opportunities to build even greater confidence and consistency in Bahasa Malaysia. To support Ah Li beautifully at home, you might try incorporating more playful exposure to Bahasa Malaysia through songs, stories, or simple daily conversations, and perhaps engage in fun number-related games together to reinforce those math skills. With your loving encouragement, Ah Li is sure to continue flourishing!', '2025-11-19 17:59:40', '2025-11-19 17:59:40');
INSERT INTO `ai_results` (`id`, `child_id`, `module`, `data`, `result`, `created_at`, `updated_at`) VALUES
(17, 12, 'learning_plan', '{\"scores\": [{\"subject\": \"math\", \"score\": 80, \"date\": \"2022-03-01\"}, {\"subject\": \"english\", \"score\": 60, \"date\": \"2022-03-01\"}, {\"subject\": \"bm\", \"score\": 70, \"date\": \"2022-03-01\"}, {\"subject\": \"math\", \"score\": 60, \"date\": \"2022-06-01\"}, {\"subject\": \"english\", \"score\": 50, \"date\": \"2022-06-01\"}, {\"subject\": \"bm\", \"score\": 40, \"date\": \"2022-06-01\"}], \"learning_result\": \"<p><strong>Most Likely Learning Style:</strong> Kinesthetic</p>\\n\\n<p>\\n    Based on the observation that the child \\\"cannot focus while study and learning at school,\\\" a kinesthetic learning style is the most likely.\\n    Kinesthetic learners thrive when they can move, touch, and interact physically with their learning environment to process information.\\n    Traditional classroom settings, which often require children to sit still for extended periods, can be particularly challenging for these active learners, leading to apparent difficulties with focus and attention.\\n    Their inherent need for movement and hands-on engagement is central to how they process and retain new information effectively.\\n</p>\\n\\n<h3>Actionable Suggestions:</h3>\\n<ul>\\n    <li>Integrate physical activity into lessons, such as movement breaks, standing desks, or learning games that involve gross motor skills.</li>\\n    <li>Provide hands-on learning opportunities using manipulatives, playdough, blocks, or other tactile materials to explore concepts.</li>\\n    <li>Encourage role-playing, experiments, and building activities where the child can actively participate and experience the learning content.</li>\\n    <li>Allow for frequent, short breaks where the child can stand up, stretch, or move around to help regulate their energy and attention.</li>\\n    <li>Utilize sensory bins or textured objects during quiet time activities to engage their tactile senses in a focused way.</li>\\n</ul>\", \"preschool_result\": \"<div style=\\\"font-family: Arial, sans-serif;\\\">\\n    <p><strong>Child\'s Age for Assessment:</strong> 68 months (5 years and 8 months)</p>\\n\\n    <h3 style=\\\"color: #4CAF50;\\\">Areas that are age-appropriate</h3>\\n    <ul>\\n        <li>No specific milestones were recorded as age-appropriate for Lam Ah Li at 68 months based on the provided data.</li>\\n    </ul>\\n\\n    <h3 style=\\\"color: #F44336;\\\">Areas that are delayed</h3>\\n    <ul>\\n        <li><strong>Movement/Physical Development:</strong> Lam Ah Li does not know how to walk at 68 months (5 years 8 months). Independent walking is typically achieved by 18 months. This represents a severe developmental delay in this area.</li>\\n        <li><strong>Social/Emotional Milestones:</strong> Lam Ah Li is recorded as \\\"Always not happy\\\" at 68 months. Typical social-emotional development for a child of this age includes expressing a range of emotions, engaging happily with others, and showing empathy. This observation suggests significant concerns regarding emotional well-being and social-emotional development.</li>\\n        <li><strong>Language/Communication:</strong> Although a \\\"test\\\" was recorded, no specific language achievements (e.g., telling stories, speaking in complex sentences, naming letters) are provided for Lam Ah Li at 68 months. For a child of this age, significant progress in verbal communication is expected. The absence of reported milestones suggests a likely delay in this area.</li>\\n    </ul>\\n\\n    <h3 style=\\\"color: #2196F3;\\\">Areas that are advanced for the child\'s age</h3>\\n    <ul>\\n        <li>No advanced milestones were recorded for Lam Ah Li based on the provided data.</li>\\n    </ul>\\n\\n    <p style=\\\"font-weight: bold; margin-top: 20px;\\\">\\n        Overall, Lam Ah Li demonstrates significant developmental delays in Movement/Physical Development and Social/Emotional Milestones, with concerns regarding Language/Communication based on the absence of reported age-appropriate achievements.\\n    </p>\\n</div>\", \"tutoring_result\": \"<h3>1. Potential Weak Areas or Skills Needing Support</h3>\\n<ul>\\n    <li><strong>Gross Motor Skills:</strong> Severe delay in walking and overall physical coordination.</li>\\n    <li><strong>Fine Motor Skills:</strong> Likely impacted due to overall motor development delays, affecting tasks requiring dexterity.</li>\\n    <li><strong>Emotional Regulation and Expression:</strong> Difficulty managing and communicating emotions, indicated by \\\"always not happy.\\\"</li>\\n    <li><strong>Social Engagement and Interaction:</strong> Challenges in connecting with peers and participating in social play, stemming from emotional well-being concerns.</li>\\n    <li><strong>Receptive and Expressive Language:</strong> Understanding spoken language and verbally communicating thoughts, needs, and ideas.</li>\\n    <li><strong>Attention and Focus:</strong> Difficulty sustaining concentration, potentially linked to her kinesthetic learning style not being met and/or underlying developmental factors.</li>\\n    <li><strong>Adaptive Skills:</strong> Basic self-care and daily living activities may be impacted by physical and cognitive delays.</li>\\n    <li><strong>Overall Cognitive Development:</strong> The presence of multiple severe delays suggests a need for comprehensive assessment and support in foundational cognitive areas.</li>\\n</ul>\\n\\n<h3>2. Subjects or Developmental Domains for Tutoring/Extra Help</h3>\\n<ul>\\n    <li><strong>Physical Therapy (PT):</strong> Absolutely essential to address the severe delay in walking, improve balance, coordination, and overall gross motor development.</li>\\n    <li><strong>Occupational Therapy (OT):</strong> Highly beneficial for sensory integration, developing fine motor skills, enhancing body awareness, and supporting adaptive daily living skills.</li>\\n    <li><strong>Speech and Language Therapy (SLT):</strong> Critical for fostering both receptive language (understanding speech) and expressive language (verbal communication, vocabulary, sentence formation).</li>\\n    <li><strong>Developmental Play Therapy / Emotional Support:</strong> To address the \\\"always not happy\\\" observation, help her understand and express emotions, develop coping strategies, and foster positive social interactions.</li>\\n    <li><strong>Early Childhood Special Education Services:</strong> A comprehensive, integrated approach focusing on all developmental domains (cognitive, social-emotional, communication, physical) with individualized educational plans.</li>\\n    <li><strong>Behavioral Support:</strong> To help manage any challenging behaviors that may arise from frustration or communication difficulties, and to teach positive behavioral strategies.</li>\\n</ul>\\n\\n<h3>3. Personalized Activity and Tutoring Style Recommendations</h3>\\n<ul>\\n    <li><strong>Movement-Integrated Learning:</strong> Embed physical activity into all learning tasks. For example, use action songs for language development, create obstacle courses that require following multi-step directions, or incorporate movement breaks every 10-15 minutes.</li>\\n    <li><strong>Hands-on and Experiential Learning:</strong> Utilize manipulatives for learning concepts (e.g., blocks for math, playdough for letter formation), sensory bins for tactile exploration (e.g., finding letters in sand), and real-life experiences (e.g., helping in the kitchen, gardening) to build vocabulary and understanding.</li>\\n    <li><strong>Role-Playing and Pretend Play:</strong> Encourage dramatic play scenarios to practice social skills, emotional expression, and language in a dynamic, engaging way. Use puppets or dress-up clothes.</li>\\n    <li><strong>Active Games and Adaptive Sports:</strong> Introduce games that are adaptable to her physical abilities to encourage participation, motor skill development, and social interaction in a fun context.</li>\\n    <li><strong>Short, Focused Sessions with Frequent Breaks:</strong> Structure learning into brief, intensive bursts (5-10 minutes) followed by active movement breaks or sensory input to help regulate attention and energy.</li>\\n    <li><strong>Multi-Sensory Approaches:</strong> Always combine visual, auditory, and kinesthetic inputs. For example, when learning new words, say the word, show a picture, and have her act it out or touch a related object.</li>\\n    <li><strong>Positive Reinforcement and Scaffolding:</strong> Provide abundant praise and positive feedback for effort and small achievements. Break down tasks into very small, manageable steps, providing hands-on assistance and gradually reducing support as she gains mastery.</li>\\n    <li><strong>Use of Visual Schedules and Timers:</strong> To help manage transitions and expectations, particularly when incorporating movement breaks, as kinesthetic learners can sometimes struggle with transitions.</li>\\n</ul>\\n\\n<p><strong>Summary for Parents or Teachers:</strong><br>\\nLam Ah Li requires a comprehensive and highly individualized support plan that prioritizes addressing her significant developmental delays across physical, social-emotional, and language domains. Given her strong kinesthetic learning style, all interventions and learning opportunities should be exceptionally active, hands-on, and engaging. Consistent collaboration with specialized therapists (Physical, Occupational, and Speech-Language) is crucial, alongside an educational approach that integrates movement, experiential learning, and sensory input into every aspect of her day. A nurturing, patient, and stimulating environment will be key to fostering her development and overall well-being.</p>\"}', '<h3>Learning Plan Summary</h3>\n<p>Lam Ah Li has a wonderful spirit and learns best when she can move, touch, and actively explore the world around her! This week, we\'ll focus on fun, playful activities that encourage gentle movement, help her express her feelings, and discover new words and ideas in a hands-on way. With your loving guidance and support, she will continue to grow and blossom beautifully every day.</p>\n\n<h3>Weekly Action Plan</h3>\n<table class=\"table table-striped\">\n  <thead>\n    <tr><th>Day</th><th>Recommended Activities</th></tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>Monday</td>\n      <td>\n        <ul>\n          <li><strong>\"Roll and Reach\" Game (15 minutes):</strong> Sit on the floor and roll a soft ball back and forth, encouraging Lam Ah Li to reach, stretch, and move her body to retrieve it.</li>\n          <li><strong>Sensory Bin Exploration (20 minutes):</strong> Fill a shallow bin with dry rice, pasta, or beans and hide small toys. Encourage her to dig, scoop, and find the treasures with her hands, naming objects as she finds them.</li>\n          <li><strong>Action Song Time (10 minutes):</strong> Sing simple songs with actions like \"If You\'re Happy and You Know It\" or \"Twinkle, Twinkle Little Star\" while helping her do the movements.</li>\n        </ul>\n      </td>\n    </tr>\n    <tr>\n      <td>Tuesday</td>\n      <td>\n        <ul>\n          <li><strong>Playdough Fun (15 minutes):</strong> Offer playdough for squishing, rolling, and making shapes. Encourage her to describe what she\'s doing (\"I\'m squishing it!\").</li>\n          <li><strong>Movement Story Time (20 minutes):</strong> Read a favorite picture book and act out parts of the story with movements, sounds, and facial expressions. Ask her to imitate or join in.</li>\n          <li><strong>\"Happy/Sad Faces\" Game (10 minutes):</strong> Use flashcards or drawings of happy, sad, angry, and surprised faces. Point to them and practice making the expressions together.</li>\n        </ul>\n      </td>\n    </tr>\n    <tr>\n      <td>Wednesday</td>\n      <td>\n        <ul>\n          <li><strong>Blanket Tunnel Crawl/Roll (15 minutes):</strong> Create a soft tunnel with blankets and cushions. Encourage her to crawl or roll through it, celebrating her movement.</li>\n          <li><strong>Building with Big Blocks (20 minutes):</strong> Use large, easy-to-grasp blocks to build towers together. Encourage her to knock them down, focusing on cause and effect and sharing.</li>\n          <li><strong>\"What\'s in the Bag?\" Mystery Game (10 minutes):</strong> Place different textured objects (e.g., a soft cloth, a bumpy toy, a smooth stone) in a bag for her to feel and describe without looking.</li>\n        </ul>\n      </td>\n    </tr>\n    <tr>\n      <td>Thursday</td>\n      <td>\n        <ul>\n          <li><strong>Bubble Catching (15 minutes):</strong> Blow bubbles and encourage her to reach, bat, and pop them from her sitting or tummy position. This promotes eye-hand coordination and gentle movement.</li>\n          <li><strong>Finger Painting Fun (20 minutes):</strong> Provide safe, washable paints and let her explore colors and textures on a large sheet of paper using her fingers and hands.</li>\n          <li><strong>Puppet Play for Feelings (10 minutes):</strong> Use simple puppets to act out different emotions or social scenarios, encouraging her to respond and express what the puppets might be feeling.</li>\n        </ul>\n      </td>\n    </tr>\n    <tr>\n      <td>Friday</td>\n      <td>\n        <ul>\n          <li><strong>Gentle Music and Movement (15 minutes):</strong> Play calming or upbeat music and encourage gentle swaying, clapping, or supported standing and rocking to the rhythm.</li>\n          <li><strong>Object Matching Game (20 minutes):</strong> Use pairs of everyday objects or large picture cards to find matches. Ask her to name the objects as she matches them.</li>\n          <li><strong>\"Tell Me About It\" with Photos (10 minutes):</strong> Look through family photos together. Point to people/things and encourage her to make sounds or use simple words to talk about them.</li>\n        </ul>\n      </td>\n    </tr>\n    <tr>\n      <td>Saturday</td>\n      <td>\n        <ul>\n          <li><strong>Outdoor Sensory Walk (15 minutes):</strong> While in a stroller or adaptive walker, gently touch leaves, grass, flowers, or smooth stones, describing their textures and colors.</li>\n          <li><strong>Water Play (20 minutes):</strong> In a shallow basin, let her play with cups for pouring, floating toys, and splashing. Supervise closely and name actions like \"pour,\" \"splash,\" \"wet.\"</li>\n          <li><strong>\"My Body Parts\" Game (10 minutes):</strong> Gently touch and name different body parts (nose, toes, hands, tummy) on herself and on you or a doll.</li>\n        </ul>\n      </td>\n    </tr>\n    <tr>\n      <td>Sunday</td>\n      <td>\n        <ul>\n          <li><strong>Guided Stretching and Movement Breaks (15 minutes):</strong> Gently guide her through simple stretches and movements, helping her explore what her body can do.</li>\n          <li><strong>Simple Puzzles (20 minutes):</strong> Engage with chunky knob puzzles or 2-3 piece puzzles, guiding her hands to fit the pieces and celebrating her success.</li>\n          <li><strong>Story Time with Props (10 minutes):</strong> Read a story and use simple props (e.g., a toy animal for an animal story) to make the experience more tactile and engaging.</li>\n        </ul>\n      </td>\n    </tr>\n  </tbody>\n</table>\n\n<h3>Long-Term Strategy</h3>\n<ul>\n  <li>**Consistent Specialist Support:** Continue attending sessions with Physical Therapists, Occupational Therapists, and Speech-Language Therapists as recommended, and integrate their exercises and advice into daily routines.</li>\n  <li>**Create an Active & Engaging Environment:** Ensure Lam Ah Li has daily opportunities for active, hands-on exploration. Use manipulatives, sensory bins, and safe spaces for gentle movement to support her kinesthetic learning style.</li>\n  <li>**Prioritize Emotional Well-being:** Regularly engage in play that helps her express feelings, using puppets, books, and verbal prompts. Create a nurturing and patient environment where her emotions are acknowledged and validated.</li>\n  <li>**Foster Communication through Play:** Integrate language learning into all activities by consistently naming objects, actions, and feelings. Respond to her attempts to communicate with enthusiasm and patience.</li>\n  <li>**Establish Predictable Routines:** Use simple visual schedules or clear verbal cues to help her anticipate and transition between activities, especially those involving movement breaks, which are crucial for her focus.</li>\n</ul>', '2025-11-19 18:14:20', '2025-11-19 18:14:20'),
(18, 12, 'resources', '{\"scores\": [{\"subject\": \"math\", \"score\": 60, \"date\": \"2022-06-01\"}, {\"subject\": \"english\", \"score\": 50, \"date\": \"2022-06-01\"}, {\"subject\": \"bm\", \"score\": 40, \"date\": \"2022-06-01\"}, {\"subject\": \"math\", \"score\": 80, \"date\": \"2022-03-01\"}, {\"subject\": \"english\", \"score\": 60, \"date\": \"2022-03-01\"}, {\"subject\": \"bm\", \"score\": 70, \"date\": \"2022-03-01\"}], \"learning_summary\": \"<p><strong>Most Likely Learning Style:</strong> Kinesthetic</p>\\n\\n<p>\\n    Based on the observation that the child \\\"cannot focus while study and learning at school,\\\" a kinesthetic learning style is the most likely.\\n    Kinesthetic learners thrive when they can move, touch, and interact physically with their learning environment to process information.\\n    Traditional classroom settings, which often require children to sit still for extended periods, can be particularly challenging for these active learners, leading to apparent difficulties with focus and attention.\\n    Their inherent need for movement and hands-on engagement is central to how they process and retain new information effectively.\\n</p>\\n\\n<h3>Actionable Suggestions:</h3>\\n<ul>\\n    <li>Integrate physical activity into lessons, such as movement breaks, standing desks, or learning games that involve gross motor skills.</li>\\n    <li>Provide hands-on learning opportunities using manipulatives, playdough, blocks, or other tactile materials to explore concepts.</li>\\n    <li>Encourage role-playing, experiments, and building activities where the child can actively participate and experience the learning content.</li>\\n    <li>Allow for frequent, short breaks where the child can stand up, stretch, or move around to help regulate their energy and attention.</li>\\n    <li>Utilize sensory bins or textured objects during quiet time activities to engage their tactile senses in a focused way.</li>\\n</ul>\", \"age\": 5, \"grade_level\": \"A\"}', '<h3>Suggested Resources Overview</h3>\nDear Parents, we\'ve put together a special collection of resources for Lam Ah Li that celebrates her energetic and hands-on learning style! Since Ah Li learns best by moving and doing, these activities are designed to be interactive and engaging. We\'ll focus on making learning Bahasa Malaysia and English fun and active, while also continuing to build on her developing math skills through playful exploration. Get ready to move, play, and discover together!\n\n<h3>Videos</h3>\n<ul>\n  <li><strong>Active Alphabet Action Song (English)</strong> – This lively video uses catchy songs and body movements to help your child learn and recognize English alphabet letters and their sounds. (Target skill: English letter recognition, phonics; approximate duration: 3-4 minutes; what parents should do: Encourage your child to sing along, mimic the actions, and even pause the video to practice forming the letters with their body or hands.)</li>\n  <li><strong>Gerak-Gerak Nombor (BM Counting Movement)</strong> – A fun Bahasa Malaysia video that teaches counting from 1 to 10 through simple, repetitive physical actions and songs. (Target skill: BM number recognition, counting, vocabulary; approximate duration: 4-5 minutes; what parents should do: Join in the movements and counts, repeating the BM words clearly. You can also point to objects around the room and count them in BM.)</li>\n  <li><strong>Shape Explorer Dance</strong> – This video encourages children to move their bodies to represent different shapes (e.g., making a circle with their arms, standing like a triangle) while identifying shapes found in their environment. (Target skill: Math - shape recognition, gross motor skills; approximate duration: 5 minutes; what parents should do: Participate with your child, helping them spot shapes around the house and encouraging creative movements for each shape.)</li>\n</ul>\n\n<h3>Games & Apps</h3>\n<ul>\n  <li><strong>Sensory Bin Letter & Number Hunt (Offline Game)</strong> – Create a large bin filled with rice, sand, or beans, and hide magnetic letters, number tiles, or small cut-out letters/numbers. Your child can use scoops or their hands to find and identify them. (Type: Offline game; target subject or skill: English/BM letter and number recognition, fine motor skills, tactile learning)</li>\n  <li><strong>Giant Floor Mat Race (Offline Game)</strong> – Use painter\'s tape to create a large number line or alphabet path on the floor. Call out a number or letter, and your child hops, skips, or crawls to it. (Type: Offline game; target subject or skill: Math - number sequencing, English/BM - letter recognition, gross motor skills)</li>\n  <li><strong>Play-Doh Story Creation (Offline Game)</strong> – Encourage your child to sculpt characters and objects from a simple story you tell in English or Bahasa Malaysia. They can act out parts of the story with their creations. (Type: Offline game; target subject or skill: English/BM vocabulary, storytelling, imaginative play, fine motor skills)</li>\n  <li><strong>Interactive Building Blocks App</strong> – A digital app that allows children to build and create structures using virtual blocks, often with challenges that involve spatial reasoning or following patterns. (Type: Mobile app / Digital game; target subject or skill: Math - spatial reasoning, problem-solving, creativity, basic physics concepts)</li>\n  <li><strong>Alphabet Tracing & Phonics Adventure</strong> – An app where children trace letters with their finger and hear the phonetic sound, often with mini-games involving matching sounds to words. (Type: Mobile app; target subject or skill: English/BM letter formation, phonics, vocabulary)</li>\n</ul>\n\n<h3>Books & Reading Materials</h3>\n<ul>\n  <li><strong>\"Busy Builders\" Lift-the-Flap Book</strong> – An interactive book where children lift flaps to discover hidden objects, numbers, or letters related to a building theme. (Reading level: Preschool; themes: Construction, discovery, numbers/letters; how it supports their learning: Encourages tactile exploration, prediction, and makes reading an active experience, engaging their kinesthetic style.)</li>\n  <li><strong>\"My First Bahasa Malaysia Words: An Action Book\"</strong> – A picture book with simple BM words and phrases, each paired with an action or movement the child can perform while reading. (Reading level: Preschool; themes: Everyday actions, BM vocabulary; how it supports their learning: Connects words to physical movements, enhancing memory and comprehension for BM.)</li>\n  <li><strong>\"Where\'s My _______?\" Sensory Board Book</strong> – Books with different textures for children to touch and feel as they search for a character or object on each page. (Reading level: Preschool; themes: Exploration, senses, animals/objects; how it supports their learning: Engages tactile senses, making reading a multi-sensory and interactive experience.)</li>\n  <li><strong>\"The Number Detective\" Interactive Picture Book</strong> – A storybook that encourages children to find and count specific objects on each page to help a character solve a mystery. (Reading level: Preschool; themes: Counting, observation, problem-solving; how it supports their learning: Turns reading into an active search-and-find game, reinforcing math skills in an engaging way.)</li>\n</ul>', '2025-11-19 18:33:21', '2025-11-20 04:01:36');

-- --------------------------------------------------------

--
-- Table structure for table `children`
--

CREATE TABLE `children` (
  `id` int(11) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `age` int(11) DEFAULT NULL,
  `grade_level` varchar(50) DEFAULT NULL,
  `gender` enum('male','female','other') DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `children`
--

INSERT INTO `children` (`id`, `parent_id`, `name`, `dob`, `age`, `grade_level`, `gender`, `notes`, `created_at`) VALUES
(10, 7, 'mee', '2023-01-02', 2, 'a', 'female', '', '2025-10-09 15:20:43'),
(11, 7, 'Tong Yi Wen', '2023-10-19', 3, 'b', 'female', '', '2025-10-13 15:55:36'),
(12, 9, 'Lam Ah Li', '2020-03-01', 5, 'A', 'female', '', '2025-11-18 18:17:18');

-- --------------------------------------------------------

--
-- Table structure for table `games`
--

CREATE TABLE `games` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `difficulty` enum('easy','medium','hard') DEFAULT 'easy',
  `url` varchar(500) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `learning_observations`
--

CREATE TABLE `learning_observations` (
  `id` int(11) NOT NULL,
  `child_id` int(11) NOT NULL,
  `observation` text NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `learning_observations`
--

INSERT INTO `learning_observations` (`id`, `child_id`, `observation`, `created_at`) VALUES
(4, 10, 'ABC', '2025-10-09 23:25:04'),
(8, 11, 'hand on activities', '2025-10-17 14:23:48'),
(9, 12, 'Cannot focus while study and learning at school', '2025-11-19 12:39:17');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `preschool_assessments`
--

CREATE TABLE `preschool_assessments` (
  `id` int(11) NOT NULL,
  `child_id` int(11) NOT NULL,
  `domain` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `preschool_assessments`
--

INSERT INTO `preschool_assessments` (`id`, `child_id`, `domain`, `description`, `date`) VALUES
(4, 10, 'Social/Emotional Milestones', 'ASSESSMENT', '2025-10-01'),
(10, 10, 'Cognitive Milestones', 'observation', '2025-11-01'),
(11, 10, 'Cognitive Milestones', 'observation', '2025-11-01'),
(12, 10, 'Cognitive Milestones', 'observation', '2025-11-01'),
(14, 12, 'Language/Communication', 'test', '2025-11-01'),
(15, 12, 'Movement/Physical Development', 'My child do not know how to walk even she is 5 years old', '2025-11-01'),
(16, 12, 'Social/Emotional Milestones', 'Always not happy', '2025-11-01');

-- --------------------------------------------------------

--
-- Table structure for table `resources`
--

CREATE TABLE `resources` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `type` enum('video','app','book','game','article') NOT NULL,
  `description` text DEFAULT NULL,
  `age_min` int(11) DEFAULT NULL,
  `age_max` int(11) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tests`
--

CREATE TABLE `tests` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tests`
--

INSERT INTO `tests` (`id`, `user_id`, `name`) VALUES
(4, 7, 'abc'),
(5, 12, 'Simple Math'),
(6, 11, 'BI test');

-- --------------------------------------------------------

--
-- Table structure for table `test_answers`
--

CREATE TABLE `test_answers` (
  `id` int(11) NOT NULL,
  `child_id` int(11) NOT NULL,
  `test_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `answer` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `test_answers`
--

INSERT INTO `test_answers` (`id`, `child_id`, `test_id`, `question_id`, `answer`, `created_at`) VALUES
(7, 11, 4, 22, '2', '2025-10-16 23:29:52'),
(8, 11, 4, 23, '3', '2025-10-16 23:29:52'),
(9, 11, 4, 24, '5', '2025-10-16 23:29:52'),
(10, 12, 5, 25, '2', '2025-11-25 17:03:35');

-- --------------------------------------------------------

--
-- Table structure for table `test_questions`
--

CREATE TABLE `test_questions` (
  `id` int(11) NOT NULL,
  `test_id` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer_type` enum('text','scale') DEFAULT 'text',
  `category` varchar(50) NOT NULL DEFAULT 'general',
  `media_type` varchar(20) DEFAULT NULL,
  `media_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `test_questions`
--

INSERT INTO `test_questions` (`id`, `test_id`, `question`, `answer_type`, `category`, `media_type`, `media_path`) VALUES
(22, 4, '1+1', 'text', 'general', NULL, NULL),
(23, 4, '2+2', 'text', 'general', NULL, NULL),
(24, 4, '3+2', 'text', 'general', NULL, NULL),
(25, 5, 'What is the answer ?', 'scale', 'reading', 'image', 'uploads/questions/test5_q1_1764058851.png'),
(26, 6, 'What is the answer ?', 'scale', 'reading', 'image', 'uploads/questions/test6_q1_1764060793.png');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('parent','admin') NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `created_at`) VALUES
(7, 'TongYi Wen', 'tongyw-wm22@student.tarc.edu.my', '$2b$12$2bBrg98cIZ4TMCVwufm2Y.tuIv/Yt9tlrWAz46gudmkeZlDfJMVKG', 'parent', '2025-09-22 15:30:50'),
(9, 'Lam Ah Kao', 'shaucharn@gmail.com', '$2b$12$Pp957FMqRboKXb.3lGkMLOEhaqglyF8qOiAK8dRmajnnx0DDMBko6', 'parent', '2025-11-18 18:15:07'),
(11, 'admin1', 'admin1@gmail.com', '$2b$12$XB07SM0yICNC8QF/51yPCOMdbV04saOYb2Z7zOQvviw8UXt8CcqLS', 'admin', '2025-11-23 16:04:06'),
(12, 'ASD', 'adminsc@gmail.com', '$2b$12$JidUcjuu7cmZ5qM7FkpHM.HmpirHYX5TmSjDR9MwJnlm.oo2.lvR.', 'admin', '2025-11-25 07:55:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_scores`
--
ALTER TABLE `academic_scores`
  ADD PRIMARY KEY (`id`),
  ADD KEY `child_id` (`child_id`);

--
-- Indexes for table `ai_results`
--
ALTER TABLE `ai_results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `child_id` (`child_id`);

--
-- Indexes for table `children`
--
ALTER TABLE `children`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Indexes for table `games`
--
ALTER TABLE `games`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `learning_observations`
--
ALTER TABLE `learning_observations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `child_id` (`child_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Indexes for table `preschool_assessments`
--
ALTER TABLE `preschool_assessments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `child_id` (`child_id`);

--
-- Indexes for table `resources`
--
ALTER TABLE `resources`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tests`
--
ALTER TABLE `tests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `test_answers`
--
ALTER TABLE `test_answers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `child_id` (`child_id`),
  ADD KEY `test_id` (`test_id`),
  ADD KEY `question_id` (`question_id`);

--
-- Indexes for table `test_questions`
--
ALTER TABLE `test_questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `test_id` (`test_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academic_scores`
--
ALTER TABLE `academic_scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `ai_results`
--
ALTER TABLE `ai_results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `children`
--
ALTER TABLE `children`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `games`
--
ALTER TABLE `games`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `learning_observations`
--
ALTER TABLE `learning_observations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `preschool_assessments`
--
ALTER TABLE `preschool_assessments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `resources`
--
ALTER TABLE `resources`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tests`
--
ALTER TABLE `tests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `test_answers`
--
ALTER TABLE `test_answers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `test_questions`
--
ALTER TABLE `test_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academic_scores`
--
ALTER TABLE `academic_scores`
  ADD CONSTRAINT `academic_scores_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `children` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `ai_results`
--
ALTER TABLE `ai_results`
  ADD CONSTRAINT `ai_results_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `children` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `children`
--
ALTER TABLE `children`
  ADD CONSTRAINT `children_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `learning_observations`
--
ALTER TABLE `learning_observations`
  ADD CONSTRAINT `learning_observations_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `children` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `preschool_assessments`
--
ALTER TABLE `preschool_assessments`
  ADD CONSTRAINT `preschool_assessments_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `children` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `tests`
--
ALTER TABLE `tests`
  ADD CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `test_answers`
--
ALTER TABLE `test_answers`
  ADD CONSTRAINT `test_answers_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `children` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `test_answers_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `test_answers_ibfk_3` FOREIGN KEY (`question_id`) REFERENCES `test_questions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `test_questions`
--
ALTER TABLE `test_questions`
  ADD CONSTRAINT `test_questions_ibfk_1` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
