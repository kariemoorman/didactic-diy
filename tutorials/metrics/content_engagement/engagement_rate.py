def content_engagement_rate(df):

    category_metrics = df.groupby('Category').agg(
        total_views=('Views', 'sum'),
        total_likes=('Likes', 'sum'),
        total_dislikes=('Dislikes', 'sum'),
    ).reset_index()

    category_metrics['like_rate'] = round(category_metrics['total_likes'] / category_metrics['total_views'], 5)
    category_metrics['dislike_rate'] = round(category_metrics['total_dislikes'] / category_metrics['total_views'], 5)
    category_metrics['like_vs_dislike_ratio'] = category_metrics['like_rate'] / category_metrics['dislike_rate']

    return category_metrics


def personal_content_engagement_rate(df):

    category_metrics = df.groupby(['Username', 'Category']).agg(
        total_videos_watched=('Views', 'sum'),
        total_likes=('Likes', 'sum'),
        total_dislikes=('Dislikes', 'sum')
    )

    category_metrics['mean_like_rate'] = round(category_metrics['total_likes']  / category_metrics['total_videos_watched'], 5)
    category_metrics['mean_dislike_rate'] = round(category_metrics['total_dislikes'] / category_metrics['total_videos_watched'], 5)
    category_metrics['like_vs_dislike_ratio'] = category_metrics['mean_like_rate'] / category_metrics['mean_dislike_rate']
    
    category_metrics.reset_index(inplace=True)

    return category_metrics
    
