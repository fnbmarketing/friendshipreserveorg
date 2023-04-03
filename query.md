

# Egg Chat
new: chat719048028657680257
old: chat497515679591336878

# Look for Group Chat

`select display_name, chat_identifier FROM chat;`



`SELECT * FROM message WHERE handle_id = (SELECT handle_id FROM chat_handle_join WHERE chat_id = (SELECT ROWID FROM chat WHERE chat_identifier = 'chat719048028657680257')) ORDER BY date DESC;`

`SELECT * FROM message WHERE handle_id = (SELECT handle_id FROM chat_handle_join WHERE chat_id = (SELECT ROWID FROM chat WHERE chat_identifier = 'chat497515679591336878')) ORDER BY date DESC;`


## Find the most react message with chat_identifier

```
SELECT reactions_egg.ROWID, reactions_egg.text, reactions_egg.phone_number, reactions_egg.guid, reactions_egg.cache_roomnames, COUNT(*) as num_reactions
FROM reactions_egg
LEFT JOIN message_attachment_join ON reactions_egg.ROWID = message_attachment_join.message_id
LEFT JOIN attachment ON message_attachment_join.attachment_id = attachment.ROWID
WHERE (attachment.mime_type = 'com.apple.emjpx' OR attachment.mime_type IS NULL)
GROUP BY reactions_egg.ROWID
ORDER BY num_reactions DESC;
```


```
SELECT text, thread_originator_guid, COUNT(*) as message_count
FROM message where thread_originator_guid is not null
GROUP BY thread_originator_guid
ORDER BY message_count DESC
LIMIT 10;
```
