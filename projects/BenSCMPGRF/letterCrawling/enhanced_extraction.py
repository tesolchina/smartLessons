#!/usr/bin/env python3
"""
Enhanced SCMP Letters Extraction with Additional Pages
This script processes the fresh content obtained via fetch_webpage to create a comprehensive corpus.
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Any

def extract_letters_from_content(content: str, page_url: str, page_title: str) -> List[Dict[str, Any]]:
    """Extract individual letters from complete webpage content"""
    
    individual_letters = []
    
    # Split content by ### headings (individual letter titles)
    sections = re.split(r'\n### ([^\n]+)\n', content)
    
    if len(sections) > 1:
        # Process pairs of (title, content)
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                letter_title = sections[i].strip()
                letter_content_raw = sections[i + 1]
                
                # Skip navigation/metadata sections
                if any(skip in letter_title.lower() for skip in 
                      ['readers discuss', 'further reading', 'related topics', 'browse other', 'discover more']):
                    continue
                
                # Extract the actual letter content and author
                content_lines = []
                author = "Unknown"
                
                # Split content into lines and process
                lines = letter_content_raw.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Skip advertisement and navigation lines
                    if any(skip in line.lower() for skip in 
                          ['advertisement', 'further reading', 'related topics', 'scmp poll', 
                           'before you go', 'discover more', 'browse other', 'follow now',
                           'start conversation', 'we use cookies']):
                        continue
                    
                    # Look for author pattern at the end
                    if (', ' in line and not line.startswith('http') and 
                        not line.startswith('www') and len(line) < 150 and
                        # Check if it looks like a name
                        re.search(r'^[A-Z][a-z]+ [A-Z]', line) and
                        # Exclude lines that are clearly content, not authors
                        not any(word in line.lower() for word in 
                               ['china', 'hong kong government', 'policy', 'should', 'must', 
                                'will', 'can', 'may', 'the', 'this', 'that', 'when', 'where',
                                'which', 'how', 'why', 'what', 'who'])):
                        author = line
                        break
                    else:
                        content_lines.append(line)
                
                # Clean up content
                letter_content = '\n'.join(content_lines).strip()
                
                # Remove author line from content if it was included
                if author != "Unknown":
                    letter_content = letter_content.replace(author, '').strip()
                
                # Only include letters with substantial content
                if letter_content and len(letter_content) > 150:
                    individual_letters.append({
                        'title': letter_title,
                        'content': letter_content,
                        'author': author,
                        'source_url': page_url,
                        'main_page_title': page_title,
                        'content_length': len(letter_content),
                        'word_count': len(letter_content.split()),
                        'extraction_timestamp': datetime.now().isoformat()
                    })
    
    # If no individual letters found using ### pattern, treat as single letter
    if not individual_letters:
        # Look for author at the end of the content
        lines = content.split('\n')
        content_lines = []
        author = "Unknown"
        
        # Look for author in the last meaningful lines
        for line in reversed(lines):
            line = line.strip()
            if (line and ', ' in line and len(line) < 150 and
                re.search(r'^[A-Z][a-z]+ [A-Z]', line) and
                not any(word in line.lower() for word in ['policy', 'should', 'government'])):
                author = line
                break
        
        # Remove author line from content
        if author != "Unknown":
            content_lines = [line for line in lines if line.strip() != author]
        else:
            content_lines = lines
            
        letter_content = '\n'.join(content_lines).strip()
        
        # Clean up content
        cleaned_lines = []
        for line in letter_content.split('\n'):
            line = line.strip()
            if (line and not any(skip in line.lower() for skip in 
                               ['advertisement', 'further reading', 'related topics', 'scmp poll',
                                'we use cookies', 'start conversation'])):
                cleaned_lines.append(line)
        
        letter_content = '\n'.join(cleaned_lines).strip()
        
        if letter_content and len(letter_content) > 150:
            individual_letters.append({
                'title': page_title.replace('Letters|', '').strip(),
                'content': letter_content,
                'author': author,
                'source_url': page_url,
                'main_page_title': page_title,
                'content_length': len(letter_content),
                'word_count': len(letter_content.split()),
                'extraction_timestamp': datetime.now().isoformat()
            })
    
    return individual_letters

def process_enhanced_corpus():
    """Process enhanced corpus with additional fetched content"""
    
    # Enhanced dataset with fetch_webpage content
    enhanced_pages = [
        {
            'url': 'https://www.scmp.com/opinion/letters/article/3324985/chinas-victory-day-parade-reminder-need-global-cooperation',
            'title': 'Letters | China\'s Victory Day parade a reminder of the need for global cooperation',
            'content': """China has just marked the 80th anniversary of its victory in the War of Resistance Against Japanese Aggression. As memories settle, the conversation shifts from ceremony to responsibility: how history can inform a more stable, rules-based international order in an era of strategic competition and rapid technological change.

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

Shevaun Gallwey, Sha Tin"""
        },
        {
            'url': 'https://www.scmp.com/opinion/letters/article/3325282/hong-kong-lawmakers-rejection-same-sex-partnership-bill-was-step-backwards',
            'title': 'Letters | Hong Kong lawmakers\' rejection of same-sex partnership bill was a step backwards',
            'content': """Hong Kong's Legislative Council has once again missed an opportunity to live up to the city's own slogan of being "Asia's World City". By rejecting the recent bill on same-sex partnerships, legislators have ensured that a minority of their fellow Hong Kong residents will continue to live without the same rights enjoyed by the majority.

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
        },
        {
            'url': 'https://www.scmp.com/opinion/letters/article/3325287/nepal-bangladesh-gen-zs-passion-must-be-paired-perspective',
            'title': 'Letters | From Nepal to Bangladesh, Gen Z\'s passion must be paired with perspective',
            'content': """What unfolded in Nepal this month and in Bangladesh last year cannot be simply framed as a reflection of Gen Z's heightened sense of conscience. While this generation is undeniably different, demanding freedom and flexibility and being exceptionally vocal about their rights, many are also deeply emotional and driven by passion. This emotional intensity, though powerful, can sometimes cloud judgment, especially when not grounded in historical context.

In Nepal, youth protests erupted after the government abruptly suspended 26 social media platforms. The move, widely seen as an attempt to silence dissent, triggered mass demonstrations. Years of economic stagnation, high youth unemployment and systemic corruption had left young Nepalis disillusioned. The protests began peacefully but later escalated after 19 people were killed in clashes with the police. Hundreds were injured. Government buildings and the homes of some political leaders were set ablaze. This tragic turn of events underscores a critical point: dissidence without clear leadership or agenda risks spiralling into chaos. The excessive use of force by authorities was unjustifiable, but so too was the destruction of public infrastructure. Many Gen Z protesters have since distanced themselves from the violence, but the damage has been done. Bangladesh offers another cautionary tale. After the country's prime minister, Sheikh Hasina, resigned on August 5, 2024, following mass student protests, the country descended into disorder. Despite the formation of an interim government, law and order remains somewhat fragile. The youth-led movement, though rooted in legitimate concerns, lacked strategic guidance and was ultimately hijacked.

In both cases, Gen Z rallied for the right reasons, against censorship, corruption and inequality. But without structure and foresight, their movements devolved into anarchy. The poor remain poor, the economy suffers and the promise of change fades.

The next generation must learn from history. Passion must be paired with perspective. Protests must be organised, inclusive and rooted in a long-term vision. Otherwise, the ideals Gen Z fights for risk being undermined by the chaos that follows."""
        },
        {
            'url': 'https://www.scmp.com/opinion/letters/article/3325177/hong-kong-no-cappadocia-balloon-fest-should-have-been-better-handled',
            'title': 'Letters | Hong Kong is no Cappadocia, but balloon fest should have been better handled',
            'content': """On Saturday, I attended the much-anticipated AIA International Hot Air Balloon Fest in Hong Kong. As someone who embraces the city's vibrant event scene, my expectations were high. Yet what unfolded was a mixed experience.

The enchanting night glow of the hot air balloons lasted only a short time before all the balloons were deflated due to safety concerns and unsettled weather amid typhoon warnings. This brief spectacle left many frustrated.

Meanwhile, the entertainment in the music zone felt somewhat one-dimensional, with predominantly Cantonese performances. For "Asia's World City", this limited cultural diversity seemed like a lost opportunity to achieve true international resonance.

Another disappointing moment was that, as far as I could tell, there was an absence of halal food options in the gourmet lane, although Hong Kong has been actively positioning itself as a Muslim-friendly tourist destination, achieving recognition this year as the "Most Promising Muslim-Friendly Destination of the Year" by CrescentRating.

One cannot help but question: what exactly makes this event "international"? The festival was promoted as Hong Kong's first international hot air balloon event, featuring balloons from Canada, the United Kingdom, Malaysia and Japan. Yet, the cultural programme was overwhelmingly local.

The focal attraction – the tethered balloon rides – was not covered by the entry tickets and, in any case, the rides did not go ahead due to licensing failures and safety concerns. This sparked public backlash and demands for refunds from those who had bought tickets. The Hong Kong Tourism Board retreated from promoting the event to stem reputational damage and the government emphasised its non-involvement in funding or organising the event."""
        }
    ]
    
    all_individual_letters = []
    
    print(f"🚀 Enhanced SCMP Letters Extraction")
    print(f"📊 Processing {len(enhanced_pages)} pages with complete content")
    print("=" * 80)
    
    for page_data in enhanced_pages:
        print(f"\n📄 Processing: {page_data['title']}")
        
        individual_letters = extract_letters_from_content(
            page_data['content'], 
            page_data['url'], 
            page_data['title']
        )
        
        print(f"   ✅ Extracted {len(individual_letters)} individual letters:")
        for letter in individual_letters:
            print(f"      - '{letter['title'][:60]}...' by {letter['author']} ({letter['word_count']} words)")
            
        all_individual_letters.extend(individual_letters)
    
    return all_individual_letters

def save_enhanced_corpus(letters: List[Dict[str, Any]], output_dir: str):
    """Save the enhanced research corpus"""
    
    # Create output directories
    json_dir = os.path.join(output_dir, 'json')
    md_dir = os.path.join(output_dir, 'markdown')
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Calculate statistics
    total_words = sum(letter['word_count'] for letter in letters)
    unique_authors = len(set(letter['author'] for letter in letters if letter['author'] != 'Unknown'))
    avg_letter_length = sum(letter['content_length'] for letter in letters) // len(letters) if letters else 0
    
    # Save individual letters
    for i, letter in enumerate(letters, 1):
        # Create safe filename
        author_safe = letter['author'].split(',')[0].replace(' ', '_').replace('.', '').replace('/', '')[:20]
        if author_safe == "Unknown" or not author_safe:
            title_safe = re.sub(r'[^\w\s-]', '', letter['title'])[:30].replace(' ', '_')
            letter_id = f"letter_{i:03d}_{title_safe}"
        else:
            letter_id = f"letter_{i:03d}_{author_safe}"
        
        # Save JSON
        json_file = os.path.join(json_dir, f"{letter_id}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(letter, f, indent=2, ensure_ascii=False)
        
        # Save Markdown
        md_file = os.path.join(md_dir, f"{letter_id}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {letter['title']}\n\n")
            f.write(f"**Author:** {letter['author']}\n\n")
            f.write(f"**Source:** {letter['source_url']}\n\n")
            f.write(f"**Main Page:** {letter['main_page_title']}\n\n")
            f.write(f"**Statistics:** {letter['word_count']} words | {letter['content_length']} characters\n\n")
            f.write(f"---\n\n")
            f.write(letter['content'])
            f.write(f"\n\n---\n\n")
            f.write(f"*Letter ID: {letter_id} | Extracted: {letter['extraction_timestamp']}*\n")
    
    # Save corpus summary
    corpus_summary = {
        'corpus_info': {
            'name': 'SCMP Letters Research Corpus - Enhanced',
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'fetch_webpage with enhanced content processing',
            'source': 'South China Morning Post - Letters to the Editor',
            'url': 'https://www.scmp.com/comment/letters'
        },
        'statistics': {
            'total_letters': len(letters),
            'total_words': total_words,
            'average_letter_length_chars': avg_letter_length,
            'average_letter_length_words': total_words // len(letters) if letters else 0,
            'unique_authors': unique_authors,
            'letters_with_known_authors': len([l for l in letters if l['author'] != 'Unknown'])
        }
    }
    
    summary_file = os.path.join(output_dir, f'enhanced_corpus_summary_{timestamp}.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(corpus_summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Enhanced Research Corpus Created!")
    print(f"📁 Location: {output_dir}")
    print(f"📊 {len(letters)} individual letters")
    print(f"📈 {total_words:,} total words")
    print(f"👥 {unique_authors} unique authors")
    print(f"📄 Summary: {summary_file}")
    
    return summary_file

def main():
    """Main execution function"""
    
    try:
        # Process enhanced corpus
        individual_letters = process_enhanced_corpus()
        
        if individual_letters:
            # Create enhanced research corpus
            output_dir = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF/enhanced_research_corpus'
            summary_file = save_enhanced_corpus(individual_letters, output_dir)
            
            print(f"\n🎉 ENHANCED EXTRACTION COMPLETED!")
            print(f"📊 Total individual letters: {len(individual_letters)}")
            print(f"📈 This demonstrates the proper methodology for full corpus creation")
            
        else:
            print("❌ No individual letters were extracted")
            
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()