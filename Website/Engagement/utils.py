def getSlugFromURL(url: str) -> str:
    url_elements_clean = []
    for el in url.split('/'):
        if len(el) > 0:
            url_elements_clean.append(el)
    return url_elements_clean[2]

#def get_root_comments(comments, root_comments:list = [], not_root_comments:list = []):
#    for comment in comments:
#        if comment not in not_root_comments:
#            if len(comment.replies.all()) > 0:
#                for n_r_c in comment.replies.all():
#                    not_root_comments.append(n_r_c)
#                get_root_comments(comment.replies.all(), root_comments, not_root_comments)
#            else:
#                root_comments.append(comment)
#        else:
#            get_root_comments(comment.replies.all(), root_comments, not_root_comments)
#
#    return root_comments

def get_root_comments(comments, root_comments:list = [], not_root_comments:list = []):
    for comment in comments:
        if len(comment.replies.all()) > 0:
            not_root_comments.append(comment)
        else:
            root_comments.append(comment)
    
    for comment in root_comments:
        if comment in not_root_comments:
            not_root_comments.append(comment)
            root_comments.remove(comment)
    
    for comment in not_root_comments:
        if comment in root_comments:
            not_root_comments.append(comment)
            root_comments.remove(comment)
        else:
            not_root_comments.remove(comment)
            root_comments.append(comment)
