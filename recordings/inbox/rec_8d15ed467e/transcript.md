---
name: Recording rec_8d15ed467e · 2026-09-29 13:42 · 31 min
type: transcript
description: Plaud recording, 31 min, 3 speakers detected; raw transcript, not yet ingested
lobe: both
sources: ["[rec_8d15ed467e 2026-09-29]"]
rec_id: rec_8d15ed467e
recorded_at: 2026-09-29T13:42:26+02:00
duration_seconds: 1877.0
speakers_detected: 3
backend: groq whisper-large-v3
transcript_version: 1
---
# rec_8d15ed467e · transcript (raw; never edited; speaker names live in speakers.md)

**SPEAKER_02** [00:00:00]
If the system is going to automatically make, set up the file, which includes making an invoice, rather than have one standard default bill language,

**SPEAKER_00** [00:00:27]
we

**SPEAKER_02** [00:00:28]
could have one for the $800 75 mm-hmm and one for the 1250 mm-hmm and I would like to have one for the engineering jobs

**SPEAKER_01** [00:00:38]
okay

**SPEAKER_02** [00:00:40]
that I set up myself

**SPEAKER_00** [00:00:42]
in

**SPEAKER_02** [00:00:43]
other words I set those I set those files up people don't book that right on Calendly yeah it's not done on calendar basis I just do it in my spare time

**SPEAKER_00** [00:00:56]
okay but

**SPEAKER_02** [00:00:57]
I'd like to have a blank that I can edit rather than write it all in so it would be something I need to call up preferably not erase from every other bill right

**SPEAKER_00** [00:01:11]
What's

**SPEAKER_02** [00:01:18]
the other thing they don't have? And what's the

**SPEAKER_00** [00:01:20]
first one? I would

**SPEAKER_01** [00:01:55]
vote for some Caprese. Yeah, I thought so. Yeah, right? I'm pretty predictable. And I will also have a club sandwich. And a mocha.

**SPEAKER_02** [00:02:06]
What's the mocha?

**SPEAKER_01** [00:02:07]
It's on the back. It says a mocha drink. So I'm guessing it's like mocha.

**SPEAKER_00** [00:02:11]
Club

**SPEAKER_01** [00:02:13]
sandwich.

**SPEAKER_00** [00:02:33]
No,

**SPEAKER_01** [00:02:34]
probably not. I could sell you a couple of bites of my sandwich too.

**SPEAKER_00** [00:02:41]
Yeah. I

**SPEAKER_01** [00:03:22]
don't

**SPEAKER_00** [00:03:24]
know.

**SPEAKER_01** [00:03:27]
I can look though. What is it, the 29th? I've given up on knowing what day of the week it

**SPEAKER_00** [00:03:46]
is.

**SPEAKER_01** [00:03:47]
I think it's the 29th. Wine tasting

**SPEAKER_00** [00:03:50]
tour.

**SPEAKER_01** [00:03:56]
dinner at the

**SPEAKER_00** [00:03:57]
winery. At the winery.

**SPEAKER_01** [00:03:58]
Yeah. Okay, I got you. And what I'm going to add to that...

**SPEAKER_00** [00:04:10]
Hold on, he's got to tell me what it

**SPEAKER_01** [00:04:12]
is. Yep. What I'm going to add to that is a small settings page where you can go edit the standard bill language so that it's not hidden in code somewhere forever. That would be

**SPEAKER_02** [00:04:26]
nice.

**SPEAKER_01** [00:04:26]
Yeah. Which will only affect things moving forward. So if you decide that whatever your standard language has gotten old, you can change it and it'll be that way moving

**SPEAKER_02** [00:04:37]
forward. Right, but it won't... I

**SPEAKER_01** [00:04:39]
don't have to do that for every bill. Nope. Nope. Every bill will start from that. And I can edit it any way I want. And then you can edit it as much as you like. But I can

**SPEAKER_02** [00:04:46]
go edit my own standard language if I want to. That's good because I was thinking that I may not dictate it exactly

**SPEAKER_01** [00:04:53]
right. Yeah, sure. So I'm going to just walk us through what I think we came to this morning. So fundamentally, we're going to take the WordPress powered system that currently does home inspection reports and consult letters. We're going to retire that in favor of a new version four on a to be determined tech stack, I'll talk to the AI about what might be the might still be WordPress and thinking not but I'll discuss pros and cons with it Doesn't much matter to you The new system will listen to Calendly and When new appointments get booked by clients online It will take all the data out of that which includes client name property address email address appointment type price and use that to create our new file which is an appointment record. Architecturally in the back side it's going to be a proper relational database so that we have a client's table that are unique and deduplicated and a properties table that's unique and deduplicated so that you can look things up and see if you've been to a property and for which clients You can look up a client and see where you've worked for them before. That's just good architecture. The file, as it were, includes all that client data. It will also generate an invoice, which is a PDF, which comes off of that template we were just talking about. The actual full bill description will come off of a big paragraph text field in the file details so you can write whatever narrative description of what you actually did was. You can also change the price. You can also edit their client details in case the email address is typed wrong or the last name is spelled wrong or whatever.

**SPEAKER_02** [00:06:51]
Yes, that does happen.

**SPEAKER_01** [00:06:52]
Yeah, and that should be way easier than the current system. Oh good. All that's just going to happen right there on page. And then the other thing it's going to do is create a, so the backbone of this rather than being WordPress posts is going to be Google Docs. So we're going to have a template Google Doc with the letterhead and stuff and the standard format for how we want to print out their address and things. And it'll create a unique copy of that with a structured file name based on client name, address. No, that's fine. That way when you're looking through Google Docs, the names of the files are self-explanatory. So it'll be year-month-date, underscore, client, last name, underscore, property address. And of course, that's only if you happen to navigate through Google Docs directly, which you'll end up doing. But also, of course, that file will be linked from the appointment details, file details. That page needs the ability to send an invoice, mark the invoices paid, resend the invoice whether it's fresh or because it's marked paid do you want it to automatically send when you mark it as paid yes the clients do you mark is paid and it just kicks it out and the client knows that you know that it's paid it seems like it just a good transactional business and housekeeping things let that happen I need to talk to the AI about or we should talk about whether it's better I I was thinking you could use the native Google share thing but I think that's clunky I think you get done with it and because you're used to managing everything from one place send deliver letter kicks out an email from that system that needs to be properly authenticated with a real email address so that we have good deliverability rather than just using the PHP mail function and I'm talking tech for it not you every now and then I'm just going to kind of wander off and come back and it should keep email logs so we can tell you you know invoice was sent this date and time letter was sent this date and time heck if we can get return receipts and know that it was delivered that'd be even better So you'll be able to go into Google Docs and copy and paste your content that you've voiced or texted into your email, because that works for you. Drop it into there and edit it. Mom can edit it. You can leave it open as long as you want. You can have multiple tabs open. None of that's dangerous or cumbersome anymore. But when it gets sent, whatever is the latest version gets sent. Gets sent, right. And the client, of course, gets read-only access. actual Google permission is anyone with the link can read

**SPEAKER_02** [00:10:02]
it. And therefore, can it go back to that original email? What will it see if I change it afterwards?

**SPEAKER_01** [00:10:13]
Whatever's new.

**SPEAKER_02** [00:10:14]
It

**SPEAKER_01** [00:10:14]
still does that? Yeah. And of course the client can print PDF very easily or, or, no, I don't want to get that complicated. You like the fact that the link updates. Let's just leave that as is. If you wanted to get complicated, we could add some kind of layer of like revised on if you go back and edit it later.

**SPEAKER_02** [00:10:48]
That's how they do building drawings. They actually have of a box in the corner that says, advise on revision. And the last one is the one that's on the page.

**SPEAKER_00** [00:10:57]
That

**SPEAKER_02** [00:10:58]
might

**SPEAKER_01** [00:10:59]
become cumbersomely complicated. All right, so we remembered invoices. We know the Google Docs pull. We're pulling from Calendly. We've got all the appointment data. We're going to have a whole,

**SPEAKER_00** [00:11:12]
you

**SPEAKER_01** [00:11:13]
and me and the AI, or me and the AI are going to have a whole different conversation about how to merge in all of the old data from the legacy systems. Sometimes you and I don't need to really talk about that. That's all in my head. Are we forgetting

**SPEAKER_02** [00:11:25]
anything? You might just want to dictate my three forms of invoices. How about

**SPEAKER_00** [00:11:30]
it?

**SPEAKER_02** [00:11:33]
Okay. Well, the $875 standard service, which is a consultation, would be, the invoice would say quote

**SPEAKER_00** [00:11:48]
structural

**SPEAKER_02** [00:11:51]
consultation including site visit

**SPEAKER_00** [00:11:55]
diagnosis

**SPEAKER_02** [00:12:02]
prescription

**SPEAKER_00** [00:12:05]
calculations

**SPEAKER_02** [00:12:13]
as necessary

**SPEAKER_00** [00:12:14]
and

**SPEAKER_02** [00:12:17]
preparation of stamped documentation letter

**SPEAKER_00** [00:12:24]
period

**SPEAKER_02** [00:12:28]
unquote

**SPEAKER_00** [00:12:29]
and

**SPEAKER_02** [00:12:31]
I can add that to say virtual site visit I can put in virtual and I can take out stamped.

**SPEAKER_01** [00:12:37]
That was the thing that we wanted to add. I think it's just healthy at the appointment level to have a three toggle of virtual site visit or design. Just that we know what the appointment type was. That was the other thing we didn't mention is the inspector dashboard view. Basically, when you log into the system, you're going to see a button that says new appointment so you can set up a new design file, a file for a design client. most recent appointments in a infinite scroll interface and link to your settings page which so far we have the invoice language on but we may come up with some other settings that we end up having in there and then the create new appointment needs to allow you to set the appointment type most of the time it's going to be design clients but for some other esoteric reasons someone didn't book the Calendly it'll work it happens yeah

**SPEAKER_02** [00:13:41]
my website by the way there are a couple of changes I need I notice in the website I don't want to bring up nice about a few things we should talk about that some other time Yeah, I'll see about that. We should probably reach for it together. It's not a very long

**SPEAKER_00** [00:14:05]
website. There's

**SPEAKER_02** [00:14:17]
stuff left over from home inspections that are clearly home inspections stuff.

**SPEAKER_01** [00:14:21]
Oh, interesting. Okay. I thought that site was newer than that, but okay. It is. But we

**SPEAKER_02** [00:14:29]
used the old site and deleted a lot of stuff, changed a lot of stuff. We did it pretty much on the

**SPEAKER_00** [00:14:37]
fly. Okay.

**SPEAKER_01** [00:14:42]
So the create new appointment gives you all the relevant fields that we need. Oh, right, and then it spawns up the Google Doc. The other thing I had mentioned is if somebody cancels their appointment through Calendly, it'll automatically go back, delete our appointment, delete the Google Doc Shell. And similarly, you should have an option to delete an appointment, whether it's a design client or if they don't go through the Calendly interface. But I can... Deleting on a Calendly is very simple. Okay. It's two things. have one and it should have you know double

**SPEAKER_02** [00:15:22]
can actually you know you do have to lead appointment

**SPEAKER_01** [00:15:24]
now

**SPEAKER_02** [00:15:25]
which I have used because basically because of certain flexibilities on the system in other words when you make this steak would use this is a quirk of the system is, you can, when you go back and correct the input data, it only corrects it for the printout. In some place, yeah, because it's scattered. You can't change the name or the input. It's scattered in too many places.

**SPEAKER_01** [00:15:51]
So you can, but you have to do it in a very specific way.

**SPEAKER_02** [00:15:54]
But it says I'm not allowed to. Oh, jeez. You're not allowed to get to this code. We're gonna lose her. Yeah, so I have to remember that certain, like Shady Lane, there is no Shady Lane, that's Shad Hill Road or something like that. Oh, okay. You know, stuff like that. And there's no way for me to change, but I'm bothering you to make a change. And I figured the heck with it. I'll figure it out. Right, right. But boy, if it's not, if it's all once instead of twice. Yeah. Then if

**SPEAKER_01** [00:16:25]
I fix something, it's just going to flatten way down. It's going to be so much simpler. So that was a problem

**SPEAKER_02** [00:16:32]
with this system and I think we'll go away with this. If I can make corrections to

**SPEAKER_01** [00:16:44]
input data that was incorrect. Okay, so that's something else we need to build into the system, which is when you change like a client name, it needs to have a trigger to know to reach into the Google Doc and change the client name in the Google

**SPEAKER_02** [00:16:59]
Doc.

**SPEAKER_01** [00:16:59]
It's

**SPEAKER_02** [00:17:00]
got to change the name of the file as well as the name on the product. Yeah.

**SPEAKER_01** [00:17:05]
That's where the problem is now. In the content of the Google Doc and in the file name of the Google Doc and in our system.

**SPEAKER_02** [00:17:12]
It'll do that. It doesn't change the file name though. Okay. Good. Thank you.

**SPEAKER_01** [00:17:19]
Oh, we should also bake into that file name. We were thinking about a very us-centric date, last name of client, address. But to To them, they also need to see it came from home directions. Okay. Wow. See, I didn't... This is the... It's so funny to me how many people in business make calendar events that say, phone call with Gordon, and then invite me to it. And, like, that is completely useless. It needs to say, Gordon Peter chat. So it makes sense to both of us. Yeah, yeah, yeah. And I'm very good about naming my calendar events, but most people aren't. website chat. I'm like, really? You know how many things on my calendar say website chat?

**SPEAKER_02** [00:18:02]
Yeah, well that's like people saying, you know, the house with the roof.

**SPEAKER_01** [00:18:06]
Really?

**SPEAKER_02** [00:18:07]
Which one was that? People do that. No, but up until now, it's all on my screen. There is no file that they see. All they see is the report. But the report's going to come out at a Google Doc.

**SPEAKER_01** [00:18:25]
What's

**SPEAKER_02** [00:18:26]
it going to look

**SPEAKER_01** [00:18:26]
like? Will it look like a

**SPEAKER_00** [00:18:28]
report?

**SPEAKER_01** [00:18:29]
It's going to look like a Google Doc. But it'll have our letterhead and stuff on it. I don't know what a Google Doc looks like. It looks like a Google Doc. It looks like a Word file. And I wonder if we can turn off the editing toolbars if you get out if you get a read-only version of something what does it look like I'll send it to myself and find out it has to it's gotta look like I was engineering a little

**SPEAKER_02** [00:18:57]
mm-hmm now does pretty good except it says septic system and sewer and stuff on it which is sort of weird mm-hmm and it was the reason we had the language information as given at the time of booking who was because so that when people told me it was a 2,000 square foot house and it had a 5,000 finished basement you don't update that because it's

**SPEAKER_01** [00:19:20]
a market time

**SPEAKER_02** [00:19:20]
okay anymore

**SPEAKER_01** [00:19:22]
right

**SPEAKER_02** [00:19:22]
right

**SPEAKER_01** [00:19:23]
exactly is it

**SPEAKER_02** [00:19:24]
relevant information at time of book you say what yeah oh and I know by the way the thing now says it's it s agent square footage I leave it blank

**SPEAKER_01** [00:19:36]
sure we don't really care about that we're doing.

**SPEAKER_02** [00:19:40]
Okay. And it says comments and I don't have any. Yep. But I could, I suppose, but I've never bothered.

**SPEAKER_00** [00:19:47]
So

**SPEAKER_02** [00:19:50]
I'm really thinking about streamlining.

**SPEAKER_01** [00:19:54]
Mm-hmm.

**SPEAKER_00** [00:19:57]
and then

**SPEAKER_01** [00:20:00]
the other thing we talked about was if

**SPEAKER_00** [00:20:02]
we

**SPEAKER_01** [00:20:04]
could migrate I would argue I mean you said about a year all the letters that you've done recently and lift them out of the old WordPress system move them forward as Google Docs so that you can go back and edit them if needed so we can truly retire this system absolutely once and be done. With a good date. Which would be interesting too because if you're never going to edit those home inspections again, right now the way people, this will get real interesting. So people have links that need to still work. And so I can set up a redirect from that link

**SPEAKER_00** [00:20:48]
and

**SPEAKER_01** [00:20:49]
have the AI go through and basically generate the report, print it to PDF, and store the PDF so that when people click their old links they get a PDF of their report. What happens now? It regenerates from the system every time. But this way that would, and in fact that's what I want to do going all the way back, all the way all the way back to 1997 Word, all those files, if it can read them and spool them as PDFs and put them into our knowledge base.

**SPEAKER_02** [00:21:23]
I started in 83. We started putting stuff on the thing in 86.

**SPEAKER_01** [00:21:28]
Yeah, and I think

**SPEAKER_02** [00:21:29]
we

**SPEAKER_01** [00:21:29]
lost

**SPEAKER_02** [00:21:31]
like 88, 89, 90, 91. Yeah, I think... But I don't think we lost 94, 95, 96.

**SPEAKER_01** [00:21:36]
No, I was just roughing it off. I think you're right. I think we go into the early 90s. But it'd be very cool if all of that just got PDFed and stored, and that way if you were looking it up or there, I guess really old stuff only you can look it up and that would retire the current system the Grayson system that's still online I don't think this system got pulled up into Grayson system and then all the old word docs and everything would just be PDF in one place and the other thing I need to do along the way now that I got talking about it is have the AI go back through all of all of my backups and try to reassemble the database that got blown apart and see if we can get that two point whatever percent data loss smaller. So Gordon, what's before? Before I print those old PDFs. Okay.

**SPEAKER_02** [00:22:31]
There are very very few instances that I would ever care about that. Except when somebody calls me about a crack in a foundation and if I've been there

**SPEAKER_00** [00:22:44]
I

**SPEAKER_02** [00:22:45]
was there 35 years ago I was there 22 years ago sometimes I was there 35 years ago and 23 years ago mm-hmm you know sometimes I wrote on the wall mm-hmm but if I have it in a report those are really interesting to

**SPEAKER_00** [00:23:00]
have yeah

**SPEAKER_01** [00:23:00]
yeah

**SPEAKER_00** [00:23:02]
Yeah,

**SPEAKER_01** [00:23:05]
so we'll go data mine all of that and in the end just create appointment records in our database so that we know who and when and where and associate that with a PDF of the final product and then all old systems can get permanently retired. Which then leads us back to search we want to be able to build a search of all that that can search by client name property address or even just show me what I did in May of 22 and have you dumped back here's all of your may of 22 appointments what do you what's your fuzzy brain trying to find yeah

**SPEAKER_02** [00:23:46]
that's probably that's an unlikely and No, I just did it recently, so it's a possibility. Oh, Richard, you smell lovely.

**SPEAKER_00** [00:23:57]
Do I?

**SPEAKER_02** [00:23:58]
You smell so nice.

**SPEAKER_00** [00:24:03]
I

**SPEAKER_02** [00:24:06]
love the smell of napalm in the morning. I mean...

**SPEAKER_00** [00:24:10]
No,

**SPEAKER_02** [00:24:13]
I like... It reminds me of the beach, and I like the beach. Do you know what I use for aftershave? sunblock only goods with with good fragrance

**SPEAKER_00** [00:24:27]
that's

**SPEAKER_02** [00:24:30]
how I buy this stuff I don't look at the numbers I just

**SPEAKER_00** [00:24:34]
that's

**SPEAKER_02** [00:24:35]
fine When's a good time for me to tell you the other bill? Go ahead. I think there's only two. Oh, no, I'm sorry. There is two of us. That was the 875. This is the 1250 beam design. It is structural consultation including site visit, evaluation of

**SPEAKER_00** [00:25:29]
different

**SPEAKER_02** [00:25:31]
beam and load path configurations calculations of chosen configuration

**SPEAKER_00** [00:25:47]
and

**SPEAKER_02** [00:25:52]
preparation of stamped

**SPEAKER_00** [00:25:55]
documentation letter.

**SPEAKER_02** [00:26:04]
Now I would like to add to that, I forgot to say, including site

**SPEAKER_00** [00:26:15]
visit,

**SPEAKER_02** [00:26:19]
calculation of loads, then it's evaluation of different and I think at the end where I say calculation of chosen configuration will I've chosen beam, column, and footing configuration. And if I don't like it exactly, I'll go to settings once and change it, because you're going to give me that option. That's so much better than relying on

**SPEAKER_01** [00:27:00]
that. Yeah, the other thing, relying on me? Definitely. Definitely. Especially, you tend to text me things, and text is the worst way to get me to do work. They're very ephemeral. Well, no. Phone calls are pretty bad, too. Phone calls are also very bad, and email is dodgy. So what is it? Email or Leah, but I'm getting better at these things. So what is

**SPEAKER_02** [00:27:22]
the best way? Because I did text because I thought it was the best way to get a hold of

**SPEAKER_01** [00:27:25]
you. I've tried to make that better for you. Or I

**SPEAKER_02** [00:27:28]
could say, I could just say call,

**SPEAKER_01** [00:27:31]
you know. No, emails are usually better and then I just have to... Or it texts you and tells you I emailed you? Yes. Or do you check your email? Oh, I check my email. I'm going to check my email right

**SPEAKER_02** [00:27:42]
now. So the third one is the more complicated one. It is. This is mine for design clients. time spent on the project at the above address

**SPEAKER_00** [00:28:08]
during

**SPEAKER_02** [00:28:22]
of including foam, no, sorry, including evaluation of Architectural drawings

**SPEAKER_00** [00:28:48]
and

**SPEAKER_02** [00:28:51]
photographs, semicolon. Phone, email, and text conversations with client, semicolon. mathematical evaluation of various

**SPEAKER_00** [00:29:11]
structural

**SPEAKER_02** [00:29:14]
configurations, semicolon. Final calculation of chosen

**SPEAKER_00** [00:29:25]
joists,

**SPEAKER_02** [00:29:34]
rafters, beams, columns. and foundations semicolon and preparation of stamped documentation letter period I'm expect that I will edit that one

**SPEAKER_00** [00:30:03]
but

**SPEAKER_02** [00:30:04]
that's but rather than but but wouldn't it be nice to edit that in settings and have that as a template

**SPEAKER_00** [00:30:09]
to

**SPEAKER_02** [00:30:10]
which I can add and subtract. That covers most of the

**SPEAKER_00** [00:30:16]
bases.

**SPEAKER_02** [00:30:21]
I think I left out calculation of loads involved or structural loads involved. Good.

**SPEAKER_01** [00:30:31]
All right. Good.

**SPEAKER_00** [00:30:34]
Alright,

**SPEAKER_01** [00:30:34]
that sounds like more than enough to get us started now that we actually got it this time.

**SPEAKER_02** [00:30:39]
Do we

**SPEAKER_01** [00:30:39]
have things on

**SPEAKER_02** [00:30:39]
order?

**SPEAKER_01** [00:30:40]
Yes. Okay. I need to find a bathroom around here. Oh yeah. I imagine there is one. It

**SPEAKER_02** [00:30:47]
would be

**SPEAKER_01** [00:30:47]
dark. These guys got it on all. I'll use my eyeballs and if that doesn't work I'll ask them. I

**SPEAKER_00** [00:31:00]
got a plug in my laptop. Oh I can't. My adapter's upstairs.

**SPEAKER_01** [00:31:08]
Eh. Cool. Thanks man. Don't want to work that hard anyway. Alright, closing out the session.

