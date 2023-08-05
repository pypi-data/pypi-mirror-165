# py-ipfs-pubsub
Pubsub client for python, since ipfshttpclient pubsub isn't compatibe with the newer versions of ipfs


# Example

	import pubsub


	# Topic specific callback
	def on_sub_test(data,seqno,topic_ids,cid):

		print ("New Message:",cid)
		print (data)
		print ("")


	# Subscribe - pubsub.sub(endpoint, topic, callback)
	pubsub.sub("/dns/127.0.0.1/tcp/5001/http","mytopic",on_sub)

	# Publish 10x
	for i in range(10):
		# Publish - pubsub.pub(endpoint, topic, str/bytes message)
		pubsub.pub("/dns/127.0.0.1/tcp/5001/http","mytopic","Hello World!")
		input("")

	# Unsubscribe from topic - pubsub.unsub(topic)
	pubsub.unsub("mytopic")