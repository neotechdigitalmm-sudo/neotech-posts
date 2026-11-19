"""
გამზადებული პოსტის დამატება / განახლება posts.json-ში (საიტის „გამზადებული პოსტები“ და კალენდარი).

გამოყენება (ამ საქაღალდიდან, ანუ მარკეტინგი\\):

  1) ახალი პოსტი (თარიღის გარეშე = „კალენდარში არ არის“, თარიღს მარკეტინგი საიტზე დანიშნავს):
     python tools/add_post.py add --id t10c --title "EZVIZ CS-T10C წყლის გაჟონვის დეტექტორი" \
        --text "D:/.../post.txt" --img "D:/.../post.png" --img "D:/.../cover.png" \
        --style 1 --where "Facebook, Instagram, YouTube" [--video "https://drive.google.com/file/d/<id>/view"] [--date 2026-11-20 --time 12:00] [--product <ბრენდ მენეჯერის პროდუქტის id>]

  2) დადების მერე ლინკების ჩაწერა (პოსტი ნაცრისფერი „გამოქვეყნდა“ ხდება):
     python tools/add_post.py posted --id t10c --link "Facebook=https://..." --link "Instagram=https://..."

  3) სია:  python tools/add_post.py list

მერე: git add -A; git commit -m "..."; git push   (და app.js-ში posts.json?v= რიცხვი გაზარდე, თუ ქეში ხელს უშლის)
სურათები მცირდება (900 px) და ინახება posts/ საქაღალდეში raw_<id>_N.jpg სახელით.
"""
import argparse, json, os, re, sys
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PJ = os.path.join(HERE, 'import', 'posts.json')
OUT = os.path.join(HERE, 'import', 'posts')


def load():
    return json.load(open(PJ, encoding='utf-8')) if os.path.exists(PJ) else []


def save(posts):
    json.dump(posts, open(PJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def shrink(src, name, w=900):
    os.makedirs(OUT, exist_ok=True)
    im = Image.open(src).convert('RGB')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name), 'JPEG', quality=82, optimize=True)
    return 'posts/' + name


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('add')
    a.add_argument('--id', required=True)
    a.add_argument('--title', required=True)
    a.add_argument('--text', help='ტექსტის ფაილი (post.txt)')
    a.add_argument('--img', action='append', default=[])
    a.add_argument('--style', default='1')
    a.add_argument('--where', default='Facebook, Instagram, YouTube')
    a.add_argument('--date')
    a.add_argument('--time', default='12:00')
    a.add_argument('--product')
    a.add_argument('--video', action='append', default=[], help='Drive-ის ვიდეოს ლინკი ან id (საიტზე Drive-ის ფლეერით ჩანს)')
    p = sub.add_parser('posted')
    p.add_argument('--id', required=True)
    p.add_argument('--link', action='append', default=[], help='ქსელი=ლინკი')
    sub.add_parser('list')
    x = ap.parse_args()

    posts = load()
    if x.cmd == 'list':
        for q in posts:
            print(q.get('id'), q.get('date'), q.get('status', 'planned'), q.get('title'))
        return
    if x.cmd == 'add':
        text = open(x.text, encoding='utf-8').read().strip() if x.text else ''
        imgs = [shrink(src, f'raw_{x.id}_{i + 1}.jpg') for i, src in enumerate(x.img)]
        entry = {'id': x.id, 'date': x.date, 'time': x.time, 'title': x.title, 'style': str(x.style), 'where': x.where,
                 'images': imgs, 'videos': [re.search(r'[-\w]{25,}', v).group(0) for v in x.video], 'text': text, 'status': 'planned', 'links': []}
        if x.product:
            entry['productId'] = x.product
        posts = [q for q in posts if q.get('id') != x.id] + [entry]
        save(posts)
        print('დაემატა:', x.id)
        return
    if x.cmd == 'posted':
        for q in posts:
            if q.get('id') == x.id:
                q['status'] = 'posted'
                q['links'] = [{'network': l.split('=', 1)[0], 'url': l.split('=', 1)[1]} for l in x.link]
                save(posts)
                print('გამოქვეყნდა:', x.id)
                return
        sys.exit('ასეთი id არ მოიძებნა: ' + x.id)


if __name__ == '__main__':
    main()
