#!/usr/bin/env python3
"""
Demo Script: Fetch fresh content for sample pages to show proper letter separation
"""

import json
import re
import os
from datetime import datetime

# Import the fetch_webpage functionality (simulated)
def demo_fetch_fresh_content():
    """Demonstrate proper extraction using fresh webpage content"""
    
    # Sample URLs to demonstrate with
    demo_urls = [
        "https://www.scmp.com/opinion/letters/article/3324985/chinas-victory-day-parade-reminder-need-global-cooperation",
        "https://www.scmp.com/opinion/letters/article/3325282/hong-kong-lawmakers-rejection-same-sex-partnership-bill-was-step-backwards"
    ]
    
    # Use the content we previously fetched with fetch_webpage tool
    demo_contents = {
        demo_urls[0]: """# Letters | China's Victory Day parade a reminder of the need for global cooperation

### Readers discuss China's commemoration of the 80th anniversary of the end of World War II, Hongkongers' engagement with the event, and a water procurement scandal

China has just marked the 80th anniversary of its victory in the War of Resistance Against Japanese Aggression. As memories settle, the conversation shifts from ceremony to responsibility: how history can inform a more stable, rules-based international order in an era of strategic competition and rapid technological change.

The arc of memory runs from the Mukden Incident on September 18, 1931, to the brutal years that followed – the Nanking massacre of 1937, the atrocities associated with Unit 731 and the widespread devastation that disrupted millions of lives. These are not merely chapters in a national narrative but core episodes in the history of wartime atrocities, demanding thorough, evidence-based remembrance lest memory drift into myth or be weaponised for today's political battles.

China's wartime mobilisation tied down substantial portions of Japan's fighting capability before the Pacific war widened the conflict across Asia. Domestic resistance made a significant contribution to the broader Allied effort.

In July 1945, China joined the Potsdam Declaration, underscoring the interconnectedness of wartime alliances and the emergence of a post-war international order, and Japan's formal surrender in September 1945 closed a brutal chapter, with Victory Day on September 3 marking remembrance and resilience.

The commemorations honoured victims and heroes while emphasising restraint and responsibility, with the parade in Tiananmen Square illustrating a mix of traditional formations and modern capabilities within a framework of peaceful development, international cooperation and commitments to global public goods.

The memory of past aggression reinforces a duty to strengthen international collaboration, guided by the United Nations Charter's principle of saving succeeding generations from the scourge of war. Some worry that displays of military modernisation may be misinterpreted as provocation. Others argue that a credible defence can be stabilised when anchored in open diplomacy and norms, provided there is predictable behaviour, transparent doctrine and active UN engagement.

For observers in the Global South, China's wartime sacrifices convey a universal message: the costs of aggression are borne by ordinary people, and sovereignty and development are inseparable from peace. The path forward demands stronger regional confidence-building, renewed multilateralism and a commitment to translating memory into action through dialogue, diplomacy and robust adherence to international norms that protect people as they pursue development and prosperity.

Muhammad Fakhrul Islam Babu, president, China Bangladesh Friendship Centre

### Hong Kong must step up patriotic education of adults

The national military parade on September 3 reminded us that the peace we currently enjoy came at a high price and that our motherland has now grown into a strong power capable of protecting its people from any kind of aggression. On September 3, some Hong Kong schools organised commemoration events to pay tribute to the Chinese people who resisted Japanese aggression 80 years ago.

I noticed when I browsed Facebook, Instagram and WeChat that, while a raft of my mainland friends shared news about or the live stream or video clips of the parade on WeChat, relatively few Hong Kong friends did the same on Facebook or Instagram.

When patriotic education is discussed, much attention is given to students with a view to cultivating a strong sense of belonging in the next generation. However, adults are unfortunately left out of the picture.

Unlike on the mainland, where people grow up learning the national language, history and culture, many adults in Hong Kong did not have the privilege of receiving such education. Also on the mainland, patriotism is part of corporate culture. Companies often take the initiative to hold patriotic and commemorative events. There is also a Unified Front Work Department which is responsible for promoting solidarity among the people.

Hong Kong society needs to devise strategies to ensure adults in the city have sufficient access to patriotic education.

A. Chan, Guangzhou

### Suspected water procurement fraud not the biggest scandal

With regard to the water procurement scandal that has provoked much discussion in recent weeks, is the scandal a distraction from the bigger outrage? Why doesn't the government simply equip offices with water filters on every floor? This would be a far more environmentally friendly and economical solution than having giant containers of water carted around.

Shevaun Gallwey, Sha Tin""",

        demo_urls[1]: """# Letters | Hong Kong lawmakers' rejection of same-sex partnership bill was a step backwards

### Readers discuss the voting down of a bill that would have recognised same-sex partnerships, the need to promote teacher well-being, and worker welfare

Hong Kong's Legislative Council has once again missed an opportunity to live up to the city's own slogan of being "Asia's World City". By rejecting the recent bill on same-sex partnerships, legislators have ensured that a minority of their fellow Hong Kong residents will continue to live without the same rights enjoyed by the majority.

No matter how we slice it, the decision is a step backward. Hong Kong has long prided itself on being outward-looking, modern and global. Yet this vote reinforces an impression of insularity at precisely the time the city can least afford it. The turmoil of 2019 and the subsequent national security crackdown have taken a toll on Hong Kong's reputation internationally. Passing this bill would have been a chance to show that the city remains aligned with modern standards and earn genuine goodwill both locally and abroad. Instead, that opportunity was incomprehensibly squandered.

And, frankly, the arguments made to derail the bill weren't particularly strong. Some lawmakers argued during the legislative process that formal recognition of same-sex couples undermines Chinese culture. This is a false premise. Sexual orientation is not a cultural phenomenon to be imported or rejected. It is a human reality, present across time, geography and tradition. By dismissing the lives of same-sex couples as merely foreign, Hong Kong diminishes its own people and writes them out of their own culture.

Recognising same-sex relationships would not have compromised Hong Kong's cultural integrity nor its Chinese identity; it would have enriched it by reflecting the diversity that has always been part of this city's story. A society confident in its heritage does not fear extending dignity to its minorities.

If Hong Kong is serious about retaining its place on the world stage, it must demonstrate not just economic vitality but also a higher degree of moral maturity.

Cesar Lardies Rivas, Cheung Sha Wan

### City must invest in teacher well-being

The Education Bureau's "Start the New School Year Full of Energy" initiative and the 4Rs Mental Health Charter – rest, relaxation, relationship and resilience – deserve recognition. These resources highlight the importance of supporting students' well-being as they face the transitions and stresses of a new academic year. They also send a welcome signal that mental health is now firmly on Hong Kong's education agenda.

Yet, for the 4Rs Charter to move from posters into practice, one critical prerequisite must not be overlooked: the well-being of teachers themselves. The research is clear. As Professor Marc Brackett of Yale University, who studies social and emotional learning (SEL), recently noted: "If SEL doesn't live in the adults, it dies in the curriculum." Studies consistently show that teacher well-being and classroom climate are linked. When teachers regulate their emotions, model healthy coping and co-regulate with students, emotional safety spreads. When teacher well-being is ignored, even the most evidence-based curricula falter.

Our frontline experience at Just Feel echoes this. Through our Compassionate School Programme, we support partner schools in cultivating compassionate school cultures. The starting point is always the adults. Teachers are first invited to practise self-compassion, strengthen their own regulation skills and experience being empathised with before guiding students. Without this foundation, efforts to build resilience and empathy in children remain superficial.

International frameworks reinforce this message. The Organisation for Economic Co-operation and Development's Teaching Compass places teacher well-being – physical, socio-emotional and cognitive – as the very anchor of teacher agency and professional competence. Crucially, it links the well-being of teachers to the same shared future vision as that of students: well-being for individuals, society and the planet. In other words, caring for teachers is inseparable from preparing the next generation to thrive.

To make the 4Rs Charter a lived reality, Hong Kong must therefore complement student-focused campaigns with a systemic, preventive and whole-school commitment to educators. This means allocating time for teacher reflection and self-care, embedding compassionate communication and social-emotional learning into professional development, and ensuring that school leaders actively prioritise staff well-being.

By investing in teachers as whole human beings, we lay the groundwork for resilient classrooms and compassionate school communities. In doing so, the 4Rs Charter will not only support students in adjusting to a new school year, but also shape a generation ready to meet the future with compassion.

Raymond Yang Sze-ngai, co-founder and executive director, Just Feel

### Rights of workers should not be sacrificed

As a concerned resident, I am writing to urge immediate action to safeguard the rights of workers in Hong Kong. The policy of importing labour, particularly amid a rising unemployment rate, appears to be exacerbating the exploitation of local workers. The practice of suppressing wages and extending working hours for workers to maximise profits must be curbed. It is imperative to ensure the livelihoods and well-being of our workforce are not sacrificed so that Hong Kong can be a good home for all.

Lawrence Choi, Tuen Mun"""
    }
    
    all_letters = []
    
    for url, content in demo_contents.items():
        print(f"\n{'='*80}")
        print(f"Processing: {url}")
        print(f"{'='*80}")
        
        # Extract letters using the ### pattern
        sections = re.split(r'\n### ([^\n]+)\n', content)
        
        if len(sections) > 1:
            # Process pairs of (title, content)
            for i in range(1, len(sections), 2):
                if i + 1 < len(sections):
                    letter_title = sections[i].strip()
                    letter_content_raw = sections[i + 1]
                    
                    # Skip the subtitle section
                    if "readers discuss" in letter_title.lower():
                        continue
                    
                    # Extract content and author
                    lines = letter_content_raw.split('\n')
                    content_lines = []
                    author = "Unknown"
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Look for author pattern
                        if (', ' in line and len(line) < 150 and 
                            re.search(r'^[A-Z][a-z]+ [A-Z]', line) and
                            not any(word in line.lower() for word in 
                                   ['china', 'hong kong', 'government', 'policy', 'should', 'must', 'the', 'this'])):
                            author = line
                            break
                        else:
                            content_lines.append(line)
                    
                    letter_content = '\n'.join(content_lines).strip()
                    
                    if author != "Unknown":
                        letter_content = letter_content.replace(author, '').strip()
                    
                    if letter_content and len(letter_content) > 100:
                        letter = {
                            'title': letter_title,
                            'content': letter_content,
                            'author': author,
                            'source_url': url,
                            'content_length': len(letter_content),
                            'word_count': len(letter_content.split())
                        }
                        
                        all_letters.append(letter)
                        
                        print(f"\n📝 Letter {len(all_letters)}:")
                        print(f"   Title: {letter_title}")
                        print(f"   Author: {author}")
                        print(f"   Length: {len(letter_content)} chars / {len(letter_content.split())} words")
                        print(f"   Preview: {letter_content[:100]}...")
    
    # Save demo results
    output_dir = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF/demo_proper_extraction'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save summary
    demo_summary = {
        'demo_extraction': {
            'timestamp': datetime.now().isoformat(),
            'note': 'This demonstrates proper extraction of individual letters from SCMP pages',
            'source_pages': len(demo_contents),
            'total_letters_extracted': len(all_letters),
            'average_letters_per_page': len(all_letters) / len(demo_contents),
        },
        'letters': all_letters
    }
    
    summary_file = os.path.join(output_dir, 'demo_proper_extraction.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(demo_summary, f, indent=2, ensure_ascii=False)
    
    # Create markdown summary
    md_file = os.path.join(output_dir, 'demo_results.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Demo: Proper SCMP Letters Extraction\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Results Summary\n\n")
        f.write(f"- **Source Pages:** {len(demo_contents)}\n")
        f.write(f"- **Individual Letters Extracted:** {len(all_letters)}\n")
        f.write(f"- **Average Letters per Page:** {len(all_letters) / len(demo_contents):.1f}\n\n")
        
        for i, letter in enumerate(all_letters, 1):
            f.write(f"## Letter {i}: {letter['title']}\n\n")
            f.write(f"**Author:** {letter['author']}\n\n")
            f.write(f"**Length:** {letter['content_length']} chars / {letter['word_count']} words\n\n")
            f.write(f"**Content:**\n{letter['content'][:300]}...\n\n")
            f.write(f"---\n\n")
    
    print(f"\n{'='*80}")
    print(f"🎉 DEMO COMPLETED!")
    print(f"📊 Extracted {len(all_letters)} individual letters from {len(demo_contents)} pages")
    print(f"📈 Average: {len(all_letters) / len(demo_contents):.1f} letters per page")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📄 Summary: {summary_file}")
    print(f"📚 Details: {md_file}")
    print(f"{'='*80}")
    
    return all_letters

if __name__ == "__main__":
    demo_fetch_fresh_content()