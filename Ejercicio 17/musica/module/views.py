from django.shortcuts import render
from module.models import *
import csv

# Create your views here.
def main(request):
    return render(request, 'index.html', {'size': 0})

def load(request):
    Artist.objects.all().delete()

    with open('data/artists.dat', 'r', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter='	')
        next(lines)

        lines = [Artist(int(id_), name, url, url_picture) for id_, name, url, url_picture in lines]
        artists = {artist.id: artist for artist in lines}

    Artist.objects.bulk_create(lines)

    Tag.objects.all().delete()

    with open('data/tags.dat', 'r') as f:
        lines = csv.reader(f, delimiter='	')
        next(lines)

        lines = [Tag(int(id_), value) for id_, value in lines]
        tags = {tag.id: tag for tag in lines}

    Tag.objects.bulk_create(lines)

    ArtistUser.objects.all().delete()

    with open('data/user_artists.dat', 'r') as f:
        lines = csv.reader(f, delimiter='	')
        next(lines)
        
        lines = [ArtistUser(user_id=int(user_id), artist=artists[int(artist_id)], listen_time=listened) for user_id, artist_id, listened in lines]
    
    ArtistUser.objects.bulk_create(lines)

    ArtistUserTag.objects.all().delete()

    with open('data/user_taggedartists.dat', 'r') as f:
        lines = csv.reader(f, delimiter='	')
        next(lines)

        lines = [ArtistUserTag(user_id=int(user_id), artist=artists[int(artist_id)], tag=tags[int(tag_id)], day=day, month=month, year=year)
                for user_id, artist_id, tag_id, day, month, year in lines if int(artist_id) in artists.keys() and int(tag_id) in tags.keys()]
        
    ArtistUserTag.objects.bulk_create(lines)

    return render(request, 'load.html', {'artist': len(Artist.objects.all()), 'tag': len(Tag.objects.all())
                                        , 'artist_user': len(ArtistUser.objects.all()), 'aut': len(ArtistUserTag.objects.all())})