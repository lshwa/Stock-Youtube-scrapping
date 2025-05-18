import argparse
import os
import json
from googleapiclient.discovery import build


def get_channel_id_by_name(youtube, channel_name):
    """
    채널 이름(예: '주식투자연구소')으로부터 channel ID 추출
    """
    search_response = youtube.search().list(
        q=channel_name,
        type="channel",
        part="snippet",
        maxResults=1
    ).execute()

    if "items" not in search_response or not search_response["items"]:
        raise ValueError(f"❌ 채널 이름 '{channel_name}' 에 대한 검색 결과가 없습니다.")

    return search_response["items"][0]["snippet"]["channelId"]


def get_uploads_playlist_id(youtube, channel_id):
    """
    channelId로부터 업로드 플레이리스트 ID 추출
    """
    res = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    if "items" not in res or not res["items"]:
        raise ValueError(f"❌ 채널 ID '{channel_id}'에 해당하는 채널 정보를 찾을 수 없습니다.")

    return res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_list(api_key, channel_name, max_results=50):
    """
    채널 이름 기반 영상 정보 가져오기
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    channel_id = get_channel_id_by_name(youtube, channel_name)
    uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)

    res = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=max_results
    ).execute()

    videos = []
    for item in res["items"]:
        snippet = item["snippet"]
        video_data = {
            "title": snippet["title"],
            "publishedAt": snippet["publishedAt"],
            "videoId": snippet["resourceId"]["videoId"],
            "description": snippet.get("description", "")
        }
        videos.append(video_data)

    return videos


def save_to_json(videos, channel_name):
    os.makedirs("data/raw_videos", exist_ok=True)
    path = f"data/raw_videos/{channel_name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(videos)} videos to {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Channel Video Scraper (by Channel Name)")
    parser.add_argument("--api_key", required=True, help="Your YouTube Data API key")
    parser.add_argument("--channel_name", required=True, help="YouTube Channel Name (or @handle)")
    parser.add_argument("--max_results", type=int, default=50, help="Number of videos to fetch")

    args = parser.parse_args()
    videos = get_video_list(args.api_key, args.channel_name, args.max_results)
    save_to_json(videos, args.channel_name)